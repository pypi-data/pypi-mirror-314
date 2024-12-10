import shutil
import click
import click_log
import json
import re
from base64 import b64decode
from re import search as regex_search
from os.path import abspath
from copy import deepcopy as clone
from convisoappsec.flowcli import help_option
from convisoappsec.flowcli.common import project_code_option
from convisoappsec.flowcli.context import pass_flow_context
from convisoappsec.logger import LOGGER
from convisoappsec.flowcli.requirements_verifier import RequirementsVerifier
from convisoappsec.flow.graphql_api.beta.models.issues.sast import (CreateSastFindingInput)
from convisoappsec.flow.graphql_api.beta.models.issues.sca import CreateScaFindingInput
from convisoappsec.common.graphql.errors import ResponseError

click_log.basic_config(LOGGER)


@click.command()
@project_code_option()
@click.option(
    "-i",
    "--input-file",
    required=True,
    type=click.Path(exists=True),
    help='The path to SARIF file.',
)
@click.option(
    "--company-id",
    required=False,
    envvar=("CONVISO_COMPANY_ID", "FLOW_COMPANY_ID"),
    help="Company ID on Conviso Platform",
)
@click.option(
    "-r",
    "--repository-dir",
    default=".",
    show_default=True,
    type=click.Path(
        exists=True,
        resolve_path=True,
    ),
    required=False,
    help="The source code repository directory.",
)
@click.option(
    '--asset-name',
    required=False,
    envvar=("CONVISO_ASSET_NAME", "FLOW_ASSET_NAME"),
    help="Provides a asset name.",
)
@help_option
@pass_flow_context
@click.pass_context
def import_sarif(context, flow_context, project_code, input_file, company_id, repository_dir, asset_name):
    context.params['company_id'] = company_id if company_id is not None else None
    context.params['repository_dir'] = repository_dir

    prepared_context = RequirementsVerifier.prepare_context(clone(context))
    asset_id = prepared_context.params['asset_id']

    try:
        conviso_api = flow_context.create_conviso_api_client_beta()
        LOGGER.info("💬 Starting the import process for the SARIF file.")
        parse_sarif_file(conviso_api, asset_id, input_file)
    except Exception as e:
        LOGGER.error(f"❌ Error during SARIF file import: {str(e)}")
        raise Exception("SARIF file import failed. Please contact support and provide the SARIF file for assistance.")


def parse_sarif_file(conviso_api, asset_id, sarif_file):
    with open(sarif_file) as file:
        sarif_data = json.load(file)

    sarif_infos = []

    for run in sarif_data['runs']:
        for rule in run.get('tool', {}).get('driver', {}).get('rules', []):
            id = rule.get('id')
            name = rule.get('name')
            references = rule.get('helpUri')
            description = rule.get('help', {}).get('text', None)

            result = {
                "id": id,
                "name": name,
                "references": references,
                "description": description
            }

            sarif_infos.append(result)

    for run in sarif_data['runs']:
        for result in run.get('results', []):
            title = None
            references = None
            description = None
            package = None
            version = None
            cve = None

            matching_info = next((info for info in sarif_infos if info['id'] == result['ruleId']), None)
            if matching_info:
                title = matching_info['name']
                references = matching_info['references']
                description = matching_info['description']

            if title is None:
                title = result.get('message').get('text', 'No title provided')

            if description is None:
               description = result.get('message', {}).get('text', 'No description provided')

            vulnerable_line = result.get('locations', {})[0].get('physicalLocation', {}).get('region', {}).get('startLine')
            severity = result.get('level', 'Unknown')
            file_name = result.get('locations', {})[0].get('physicalLocation', {}).get('artifactLocation', {}).get('uri')
            code_snippet = result.get('locations', {})[0].get('physicalLocation', {}).get('contextRegion', {}).get('snippet', {}).get('text', '')
            first_line = result.get('locations', {})[0].get('physicalLocation', {}).get('region', {}).get('startLine', 1)

            if "(sca)" in result.get('ruleId'):
                title = result.get('message', {}).get('text')
                package = title.split(':')[1].split(' ')[0]
                version = package.split('-')[-1]
                cve = title.split(' ')[1].strip('()')

                create_sca_vulnerabilities(
                    conviso_api, asset_id, title, references, description,
                    severity, file_name, first_line, package, version, cve
                )

            if "(sast)" in result.get('ruleId'):
                create_sast_vulnerabilities(
                    conviso_api, asset_id, title, references, description, vulnerable_line, severity, file_name,
                    code_snippet, first_line, cve
                )

    LOGGER.info("✅ SARIF file import completed successfully.")


def create_sast_vulnerabilities(conviso_api, asset_id, *args):
    title, references, description, vulnerable_line, severity, file_name, code_snippet, first_line, cve = args

    issue_model = CreateSastFindingInput(
        asset_id=asset_id,
        file_name=file_name,
        vulnerable_line=vulnerable_line,
        title=title,
        description=description,
        severity=severity,
        commit_ref=None,
        deploy_id=None,
        code_snippet=parse_code_snippet(code_snippet),
        reference=parse_conviso_references(references),
        first_line=first_line,
        category=None,
        original_issue_id_from_tool=None
    )

    try:
        conviso_api.issues.create_sast(issue_model)
    except ResponseError as error:
        if error.code == 'RECORD_NOT_UNIQUE':
            pass
        else:
            raise error # TODO send a notification to conviso slack
    except Exception:
        pass


def create_sca_vulnerabilities(conviso_api, asset_id, *args):
    title, references, description, severity, file_name, first_line, package, version, cve = args

    issue_model = CreateScaFindingInput(
        asset_id=asset_id,
        title=title,
        description=description,
        severity=severity,
        solution="Update to the last package version.",
        reference=references,
        file_name=file_name,
        affected_version=version,
        package=package,
        cve=cve,
        patched_version='',
        category='',
        original_issue_id_from_tool=''
    )

    try:
        conviso_api.issues.create_sca(issue_model)
    except ResponseError as error:
        if error.code == 'RECORD_NOT_UNIQUE':
            pass
    except Exception:
        pass


def parse_code_snippet(code_snippet):
    try:
        decoded_text = b64decode(code_snippet).decode("utf-8")
        lines = decoded_text.split("\n")
        cleaned_lines = []

        for line in lines:
            cleaned_line = line.split(": ", 1)[-1]
            cleaned_lines.append(cleaned_line)

        code_snippet = "\n".join(cleaned_lines)

        return code_snippet
    except Exception:
        return code_snippet


def parse_conviso_references(references=[]):
    if not references:
        return ""

    DIVIDER = "\n"

    references_to_join = []

    for reference in references:
        if reference:
            references_to_join.append(reference)

    return DIVIDER.join(references_to_join)

def parse_first_line_number(encoded_base64):
    decoded_text = b64decode(encoded_base64).decode("utf-8")

    regex = r"^(\d+):"

    result = regex_search(regex, decoded_text)

    if result and result.group(1):
        return result.group(1)

    LINE_NUMBER_WHEN_NOT_FOUND = 1
    return LINE_NUMBER_WHEN_NOT_FOUND


import_sarif.epilog = '''
'''
EPILOG = '''
Examples:

  \b
  1 - Import results on SARIF file to Conviso Platform:
    $ export CONVISO_API_KEY='your-api-key'
    $ export CONVISO_PROJECT_CODE='your-project-code'
    $ {command} --input-file /path/to/file.sarif

'''  # noqa: E501

SHORT_HELP = "Perform import of vulnerabilities from SARIF file to Conviso Platform"

command = 'conviso findings import-sarif'
import_sarif.short_help = SHORT_HELP
import_sarif.epilog = EPILOG.format(
    command=command,
)
