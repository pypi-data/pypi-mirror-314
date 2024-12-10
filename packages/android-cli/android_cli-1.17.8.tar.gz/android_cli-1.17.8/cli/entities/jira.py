import json
import re
import sys
import threading
import time

import requests
from requests.auth import HTTPBasicAuth

from cli.entities.setting import Settings
from cli.utils.singleton import singleton

JIRA_TRANSITIONS = {
    'BACKLOG': '11',
    'BLOCKED': '51',
    'DISCARDED': '52',
    'PLANNING': '65',
    'DOING': '63',
    'TESTING': '58',
    'READY_FOR_PROD': '64',
    'PRE_PROD': '61',
    'DONE': '5'
}


def show_loading_spinner(is_loading, message="Loading, please wait ..."):
    spinner = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
    while is_loading.is_set():
        for char in spinner:
            sys.stdout.write(f'\r{char} {message}')
            time.sleep(0.1)
            sys.stdout.flush()
    sys.stdout.write('\r' + ' ' * 100 + '\r')
    sys.stdout.flush()


@singleton
class Jira:

    def __init__(self, settings=Settings()):
        self.credentials = settings.get_jira_credentials()
        self.auth = HTTPBasicAuth(self.credentials['user'], self.credentials['token'])
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

    @staticmethod
    def make_get_request(self, api_endpoint, query=None, method="GET", data=None):
        if query is None:
            query = {}
        if data is None:
            data = {}
        return requests.request(
            method,
            self.credentials['url_base'] + api_endpoint,
            data=data,
            headers=self.headers,
            auth=self.auth,
            params=query
        )

    # @staticmethod
    def get_user_id(self):
        api_endpoint = f'/rest/api/3/myself'

        response = self.make_get_request(self, api_endpoint)
        user_info = response.json()

        return user_info.get("accountId")

    @staticmethod
    def get_transitions(self, issue_key):
        api_endpoint = f'/rest/api/3/issue/{issue_key}/transitions'

        response = self.make_get_request(self, api_endpoint)

        if response.status_code == 200:
            transitions = response.json().get('transitions')
            result = ""
            for transition in transitions:
                result = result + f"{transition['name']}: {transition['id']},"
            return result
        else:
            return "Error getting transactions"

    @staticmethod
    def make_transition(self, issue_key, transition_id):
        api_endpoint = f'/rest/api/3/issue/{issue_key}/transitions'

        payload = json.dumps({
            "transition": {"id": transition_id}
        })

        response = self.make_get_request(self, api_endpoint, method="POST", data=payload)

        if response.status_code == 204:
            return f"Issue: {issue_key} updated successfully"
        else:
            print(response.json())
            return "Error updating issue:"

    def delete_ticket(self, issue_key):
        api_endpoint = f'/rest/api/3/issue/{issue_key}'

        response = self.make_get_request(self, api_endpoint, method="DELETE")

        if response.status_code == 204:
            return "Issue deleted successfully"
        else:
            print(response.text)
            return f"Error deleting issue {issue_key}: {response.status_code}"

    def create_ticket(self, project_id, title, squad, description=""):
        api_endpoint = f'/rest/api/3/issue'

        if project_id == "BUG":
            issue_type = "Bug"
        else:
            issue_type = "Epic"

        account_id = self.get_user_id()

        fields = {
            "project": {"key": project_id},
            "summary": f'[Android] {title}',
            "issuetype": {"name": issue_type},
            "components": [{"name": "Android"}],
            "labels": ["IT"],
            "customfield_10278": {'value': squad},
            "assignee": {"id": account_id}
        }

        if description:
            fields["description"] = {
                "type": "doc",
                "version": 1,
                "content": [{
                    "type": "paragraph",
                    "content": [{
                        "text": description,
                        "type": "text"
                    }]
                }]
            }

        payload = {"fields": fields}

        payload_json = json.dumps(payload)

        response = self.make_get_request(self, api_endpoint, method="POST", data=payload_json)
        if response.status_code == 201:
            issue_data = response.json()
            issue_key = issue_data.get("key")
            self.make_transition(self, issue_key, JIRA_TRANSITIONS['BACKLOG'])
            return f'<gray>URL</gray>: \n<y>{self.credentials["url_base"]}/browse/{issue_key}</y>'
        else:
            print(response.text)
            return "Error creating ticket"

    def get_projects(self):
        api_endpoint = f'/rest/api/3/project'

        request = self.make_get_request(self, api_endpoint)
        projects = request.json()

        return projects

    def update_pr_field(self, key, pr_url):
        api_endpoint = f'/rest/api/3/issue/{key}'

        adf_payload = {
            "version": 1,
            "type": "doc",
            "content": [
                {
                    "type": "paragraph",
                    "content": [
                        {
                            "type": "text",
                            "text": pr_url
                        }
                    ]
                }
            ]
        }

        payload = json.dumps({
            "fields": {
                "customfield_10208": adf_payload
            }
        })

        self.make_get_request(self, api_endpoint, method="PUT", data=payload)

    def get_ticket_by_key(self, key):
        query = {'fields': ['id', 'key', 'summary', 'customfield_10208', 'duedate']}
        api_endpoint = f'/rest/api/3/issue/{key}'

        response = self.make_get_request(self, api_endpoint, query)

        if response.status_code == 200:
            data = response.json()
            if data:
                tickets = [data]
                return tickets
            else:
                return []
        else:
            return []

    def get_tickets_by_status(self, status):
        jql_query = f'status = "{status}" AND component = "Android"'
        query = {
            'jql': jql_query,
            'maxResults': 100,
            'fields': ['id', 'key', 'summary']
        }
        api_endpoint = '/rest/api/3/search'

        response = self.make_get_request(self, api_endpoint, query)

        if response.status_code == 200:
            data = response.json()
            if 'issues' in data:
                return data['issues']
            else:
                return []
        else:
            return []

    def get_release_active_android_release(self, key="PR"):
        api_endpoint = f'/rest/api/3/project/{key}/versions'

        response = self.make_get_request(self, api_endpoint)

        if response.status_code == 200:
            versions = response.json()
            pattern = re.compile(r"\[android]", re.IGNORECASE)
            active_versions = [
                v for v in versions
                if not v.get('archived', True)
                   and not v.get('released', True)
                   and pattern.search(v.get('name', ''))
            ]
            if active_versions:
                return active_versions[0]
            else:
                print("No se encontraron versiones activas")
        else:
            print("Error al obtener versiones:", response.status_code)

    def get_issues_by_release_version(self, version: str):
        jql_query = f'fixVersion = "{version}"'
        query = {'jql': jql_query}

        api_endpoint = '/rest/api/3/search'

        response = self.make_get_request(self, api_endpoint, query)

        if response.status_code == 200:
            issues = response.json()['issues']
            for issue in issues:
                print(f"Issue ID: {issue['id']}, Key: {issue['key']}, Summary: {str(issue['fields']['summary']).strip()}")
        else:
            print(f"Error al obtener issues: {response.status_code}")

    def get_issues_by_target_date(self, targetdate, project_keys=['PR']):
        project_filter = f'project IN ({", ".join(f"""{key}""" for key in project_keys)})'

        jql_query = f'{project_filter} AND component = "Android" AND targetdate = "{targetdate}"'
        query = {'jql': jql_query}

        api_endpoint = '/rest/api/3/search'

        response = self.make_get_request(self, api_endpoint, query)

        if response.status_code == 200:
            issues = response.json().get('issues', [])
            return issues
        else:
            print(f"Error al obtener issues: {response.status_code}")

    def create_release(self, version_name, description="", project_key="PR"):
        api_endpoint = '/rest/api/3/version'

        payload = {
            "name": f'[Android] {version_name}',
            "description": description,
            "archived": False,
            "released": False,
            "project": project_key
        }

        response = self.make_get_request(self, api_endpoint, method="POST", data=json.dumps(payload))

        if response.status_code == 201:
            print(response.json())
            print("Versión creada con éxito.")
        else:
            print(response.json())
            print(f"Error al crear la versión: {response.status_code}")

    def update_issue_with_fix_version(self, issue_key, fix_version_id):
        api_endpoint = f'/rest/api/3/issue/{issue_key}'
        active_release = self.get_release_active_android_release()
        version = active_release.get('id')
        payload = {
            "update": {
                "fixVersions": [
                    {"add": {"id": version}}
                ]
            }
        }

        response = self.make_get_request(self, api_endpoint, method="PUT", data=json.dumps(payload))

        if response.status_code == 204:
            print(f"El issue {issue_key} ha sido actualizado con el fix version {fix_version_id}.")
        else:
            print(response.json())
            print(f"Error al actualizar el issue {issue_key}: {response.status_code}")

    def update_release_description(self, issues):
        active_release = self.get_release_active_android_release()
        version = active_release.get('id')
        api_endpoint = f'/rest/api/3/version/{version}'

        issue_descriptions = [f"[{issue['key']}] {str(issue['fields']['summary']).strip()}" for issue in issues]
        new_description = "\n".join(issue_descriptions)
        payload = {
            "description": new_description
        }

        response = self.make_get_request(self, api_endpoint, method="PUT", data=json.dumps(payload))

        if response.status_code in [200, 204]:
            print("La descripción del release ha sido actualizada con éxito.")
        else:
            print(f"Error al actualizar la descripción del release: {response.status_code}")

    def create_release_and_add_issues(self, issues_target_date, version_name):
        is_loading = threading.Event()
        is_loading.set()

        spinner_thread = threading.Thread(target=show_loading_spinner, args=(is_loading, "Creating release ..."))
        spinner_thread.start()

        try:
            self.create_release(version_name=version_name)
        finally:
            is_loading.clear()
            spinner_thread.join()

        is_loading = threading.Event()
        is_loading.set()

        spinner_thread = threading.Thread(target=show_loading_spinner, args=(is_loading, "Adding tickets ..."))
        spinner_thread.start()

        try:
            issues = self.get_issues_by_target_date(targetdate=issues_target_date)
            for issue in issues:
                self.update_issue_with_fix_version(issue.get('key'), version_name)
        finally:
            is_loading.clear()
            spinner_thread.join()

        spinner_thread = threading.Thread(target=show_loading_spinner, args=(is_loading, "Creating description ..."))
        spinner_thread.start()

        try:
            issues = self.get_issues_by_target_date(targetdate=issues_target_date, project_keys=['PR', 'NPR', 'BUG', 'SEC', 'EM'])
            self.update_release_description(issues)
        finally:
            is_loading.clear()
            spinner_thread.join()
            return "Release created"

    def update_release_tickets_live(self):
        is_loading = threading.Event()
        is_loading.set()

        spinner_thread = threading.Thread(target=show_loading_spinner, args=(is_loading, "Updating tickets status ..."))
        spinner_thread.start()

        try:
            active_release = self.get_release_active_android_release()
            ticket_key = self.search_key_in_description(active_release.get('description'))
            ticket = self.get_ticket_by_key(ticket_key)[0].get('fields')
            target_date = ticket.get('targetdate')
            issues = self.get_issues_by_target_date(target_date, project_keys=['PR', 'NPR', 'BUG', 'SEC', 'EM'])
            for issue in issues:
                ticket_key = issue.get('key')
                transition = self.make_transition(self, issue_key=ticket_key, transition_id=JIRA_TRANSITIONS['DONE'])
                print(transition)
        finally:
            is_loading.clear()
            spinner_thread.join()
            return "Tickets updated"

    @staticmethod
    def search_key_in_description(description):
        match = re.search(r'\[(PR-|BUG-|NPR-|SEC-)\d+\]', description)

        if match:
            return match.group(0)[1:-1]
        else:
            print("No se encontró un patrón [PR|BUG|NPR|SEC-XXXX] en el texto.")
