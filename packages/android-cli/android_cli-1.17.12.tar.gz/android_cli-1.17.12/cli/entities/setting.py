import base64
import os
import json

from cli.entities.git import Git
from cli.utils.singleton import singleton
from cli.utils.ui import UI

DIR_NAME = '.androidcli'
DEFAULT_FILE_NAME = 'config-cli.json'
DEFAULT_SETTING = {
    "aws_region": "us-east-1",
    "aws_profile": 'username',
    "use_uuid_token_for_pull_request": False,
    "commit_setting": {
        "types": [
            {"enabled": True, "name": "feat: A new feature", "value": "feat"},
            {"enabled": True, "name": "fix: A bug fix", "value": "fix"},
            {"enabled": False, "name": "refactor: A code change (non new feature or fix) ", "value": "refactor"},
            {"enabled": False, "name": "docs: Documentation only changes", "value": "docs"},
            {"enabled": False, "name": "style: Changes that do not affect the meaning of the code", "value": "style"},
            {"enabled": False, "name": "perf: A code change that improves performance", "value": "perf"},
            {"enabled": False, "name": "test: Adding missing tests", "value": "test"},
            {"enabled": False,
             "name": "chore: Changes to the build process or auxiliary tools and libraries such as documentation generation",
             "value": "chore"},
            {"enabled": False, "name": "ci: Changes to our CI configuration files and scripts", "value": "ci"},
            {"enabled": False, "name": "revert: Reverts a previous commit", "value": "revert"},
            {"enabled": False, "name": "test: Adding testing", "value": "test"}
        ],
        "scopes": ["global",
                   "events",
                   "i18n",
                   "crypto",
                   "fans-corner",
                   "debit",
                   "pix",
                   "architecture",
                   "purchase",
                   "withdrawal",
                   "axp",
                   "voucher",
                   "rewards",
                   "lottery"]
    },
    "branch_setting": {
        "bloqued_branches": ["master", "release", "develop", "main"],
        "release_branch": "develop",
        "develop_branch": "depoy/tst",
        "types": [
            {"enabled": True, "name": "feature", "value": "feature"},
            {"enabled": True, "name": "fix", "value": "fix"},
        ],
    },
    "jira": {
        'user': 'username',
        'token': 'token',
        'url_base': 'https://astropayglobal.atlassian.net'
    },
    "lokalise": {
        'api_token': "api_token",
        'project_id': "project_id"
    },
    "bitrise": {
        "prod": {
            "build_trigger_token": "",
            "curl_url_id": ""
        },
        "test": {
            "build_trigger_token": "",
            "curl_url_id": ""
        }
    },
    "firebase_id": ""
}

firebase_id_key = {"firebase_id": ""}


@singleton
class Settings:
    directory = os.path.join(os.path.expanduser('~'), DIR_NAME)
    file_path = os.path.join(directory, DEFAULT_FILE_NAME)
    use_custom = False
    config = None

    def init(self):
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)

        if not os.path.exists(self.file_path):
            with open(self.file_path, "w") as config_file:
                json.dump(DEFAULT_SETTING, config_file, indent=4)

        self.load()

    def load(self):
        with open(self.file_path, "r") as config_file:
            self.config = json.load(config_file)

        new_key = next(iter(firebase_id_key))
        if new_key not in self.config:
            self.config.update(firebase_id_key)
            with open(self.file_path, "w") as config_file:
                json.dump(self.config, config_file, indent=4)

        return self.config

    def save(self):
        with open(self.file_path, "w") as config_file:
            json.dump(self.config, config_file, indent=4)
        return self.config

    def get_jira_credentials(self):
        return self.config['jira']

    def get_lokalise_credentials(self):
        return self.config['lokalise']

    def get_bitrise_credentials(self):
        return self.config['bitrise']

    def print(self):
        self.load()

        def print_types(types):
            result = ''
            for type in types:
                if type["enabled"]:
                    value: str = type["value"].split(":")[0]
                    result += f'\033[33m{value}\033[0m, '
                else:
                    value: str = type["value"].split(":")[0]
                    result += f'\033[90m{value}\033[0m, '
            return result[:-2]

        def print_scopes():
            scopes = Settings().config["commit_setting"]["scopes"]
            result = ''
            for scope in scopes:
                result += f'\033[33m{scope}\033[0m, '

            return result[:-2]

        header_title = "Settings"
        repository_name = Git().get_repository_name(False)
        header_sub_text = f""
        if self.use_custom:
            header_sub_text = f"<gray>{repository_name}.json</gray>"

        UI().clear()
        UI().pline_top(len(header_title) + 4)
        UI().ptext(f"│ <reverse> {header_title} </reverse> │ {header_sub_text}")

        UI().pline()

        UI().ptext(f"│ menu mode: <y>{mode}</y>")
        UI().ptext(f"│ editor: <y>{Settings().config['editor']}</y>")
        UI().pline_middle_(10)
        UI().ptext(f"│ aws_profile: <y>{format(self.config['aws_profile'])}</y>")
        UI().ptext(f"│ aws_region: <y>{format(self.config['aws_region'])}</y>")
        UI().pline_middle_(10)
        UI().ptext(f"│ <bold>Branch setting</bold>")
        UI().ptext(f"│ - Bloqued Branch: <y>{format(Settings().config['branch_setting']['bloqued_branches'])}</y>")
        UI().ptext(f"│ - Release Branch: <y>{format(Settings().config['branch_setting']['release_branch'])}</y>")
        UI().ptext(f"│ - Develop Branch: <y>{format(Settings().config['branch_setting']['develop_branch'])}</y>")
        UI().ptext(f"│ - types: {print_types(Settings().config['branch_setting']['types'])}")
        UI().pline_middle_(10)
        UI().ptext(f"│ <bold>Commit setting</bold>")
        UI().ptext(f"│ - types: {print_types(Settings().config['commit_setting']['types'])}")
        UI().ptext(f"│ - scopes: {print_scopes()}")
        UI().pline_middle_(10)
        UI().ptext(f"│ repository name: <y>{repository_name}</y>")
        UI().ptext(f"│ Setting File: <g>{self.file_path}</g>")
        UI().pline()
        UI().pcontinue()

