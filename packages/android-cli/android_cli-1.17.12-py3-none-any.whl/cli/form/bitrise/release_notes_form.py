import re

import questionary

from cli.utils.configs import BuildType
from cli.entities.jira import Jira


def extract_jira_key(branch):
    regex = r'/([A-Za-z]+-\d+)/'

    matches = re.search(regex, branch)

    if matches:
        return matches.group(1)
    else:
        return None


def get_release_notes_form(build_type: BuildType, branch):
    jira = Jira()

    if build_type == BuildType.RELEASE:
        tickets = jira.get_tickets_by_status("PRE PROD")
    elif build_type == BuildType.RELEASE_QA_TESTS:
        tickets = jira.get_tickets_by_status("PRE PROD")
    elif build_type == BuildType.F_AND_F:
        tickets = jira.get_tickets_by_status("PRE PROD")
    else:
        tickets = jira.get_ticket_by_key(extract_jira_key(branch))

    if tickets:
        release_notes = [f"[{ticket['key']}] {str(ticket['fields']['summary']).strip()}" for ticket in tickets]

        if build_type == BuildType.RELEASE_QA_TESTS:
            return '\\\\n'.join(release_notes).replace("'", "")
        else:
            return '\n'.join(release_notes)
    else:
        try:
            release_notes = questionary.unsafe_prompt(
                {
                    'type': 'text',
                    'name': 'value',
                    'message': 'Write the release notes, separated by commas:',
                    'default': '',
                    'validate': lambda val: 'You should add one release note at least' if not validate_release_note(
                        val) else True
                }
            )
            return release_notes['value'].replace(',', '\n')
        except KeyboardInterrupt:
            return -1


def validate_release_note(value):
    if value:
        return True
    else:
        return False
