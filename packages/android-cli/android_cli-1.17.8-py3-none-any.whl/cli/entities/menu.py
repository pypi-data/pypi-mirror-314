import base64
import os

from cli.entities.aws import Aws
from cli.entities.fcm import FCM
from cli.entities.jira import Jira
from cli.form._form_confirm import confirm_question
from cli.form.code_gen.code_gen_form import get_code_gen_menu_form
from cli.form.code_gen.create_new_screen import create_new_screen
from cli.form.code_gen.create_new_module import create_new_module
from cli.form.fcm.fcm_firebase_id_form import ask_for_firebase_id
from cli.form.fcm.fcm_notification_action_form import ask_for_notification_action
from cli.form.fcm.fcm_notification_body_form import ask_for_notification_body
from cli.form.fcm.fcm_notification_deeplink_form import ask_for_notification_deeplink
from cli.form.fcm.fcm_notification_title_form import ask_for_notification_title
from cli.form.git.create_new_branch import create_new_branch_from_release_branch
from cli.form.git.create_new_pull_request import create_new_pull_request
from cli.form.git.git_form import get_git_menu_form
from cli.form.jira.jira_description_form import ask_for_issue_description
from cli.form.jira.jira_issue_form import get_jira_issue_form
from cli.form.jira.jira_release_start_date_form import ask_for_release_start_date
from cli.form.jira.jira_release_version_form import ask_for_release_version
from cli.form.jira.jira_title_form import ask_for_issue_title
from cli.form.jira.jira_issue_squad_form import get_jira_issue_squad_form
from cli.form.lokalise.lokalise_menu_form import get_lokalise_menu_form
from cli.entities.bitrise import Bitrise
from cli.utils.configs import BuildType
from cli.entities.app import App
from cli.form.bitrise.branch_form import get_branch_form
from cli.form.bitrise.build_type_form import get_build_type_form
from cli.form.bitrise.release_notes_form import get_release_notes_form
from cli.form.bitrise.version_code_form import get_version_code_form
from cli.form.bitrise.version_name_form import get_version_name_form
from cli.utils.ui_menu import UIMenu, UIMenuOptions
from cli.utils.singleton import singleton
from cli.utils.ui import UI


@singleton
class Menu:

    # FIRST MENU ------------------------------------
    @staticmethod
    def bitrise_menu():
        UI().clear()
        UI().pheader(f"BITRISE CONFIGURATIONS")
        UI().pline()
        UI().ptext('<g>New Build</g>')

        build_type_form_result = get_build_type_form()
        if build_type_form_result == -1:
            return
        else:
            build_type: BuildType = BuildType.from_string(build_type_form_result)

        branch_form_result = get_branch_form()
        if branch_form_result == -1:
            return
        else:
            branch = branch_form_result

        release_notes_form_result = get_release_notes_form(build_type, branch)
        if release_notes_form_result == -1:
            return
        else:
            release_notes = release_notes_form_result

        version_code = ""
        version_name = ""

        if build_type == BuildType.RELEASE:
            release_curl = Bitrise().generate_release_curl(branch, release_notes)
        elif build_type == BuildType.RELEASE_QA_TESTS:
            release_curl = Bitrise().generate_release_qa_tests_curl(branch, release_notes)
        else:
            version_code_form_result = get_version_code_form(build_type)
            if version_code_form_result == -1:
                return
            else:
                version_code = version_code_form_result

            version_name_form_result = get_version_name_form(build_type)
            if version_name_form_result == -1:
                return
            else:
                version_name = version_name_form_result

            env = "test"
            if build_type == BuildType.F_AND_F or build_type == BuildType.PROD_FEATURE_BRANCH:
                env = "prod"
            release_curl = Bitrise().generate_feature_branch_curl(branch, release_notes, version_name, version_code,
                                                                  env)

        print("")
        print(release_curl)
        print("")

        confirm = confirm_question(message=f"Do you want to execute the curl?")

        if confirm:
            if build_type == BuildType.RELEASE:
                Bitrise().execute_release_curl(branch, release_notes)
            elif build_type == BuildType.RELEASE_QA_TESTS:
                Bitrise().execute_release_qa_tests_curl(branch, release_notes)
            else:
                env = "test"
                if build_type == BuildType.F_AND_F or build_type == BuildType.PROD_FEATURE_BRANCH:
                    env = "prod"
                Bitrise().execute_feature_branch_curl(branch, release_notes, version_name, version_code, env)

        UI().pline()
        UI().pcontinue()

    @staticmethod
    def fcm_menu():
        UI().clear()
        UI().pheader(f"FCM")
        UI().pline()
        UI().ptext('<g>Send push</g>')

        firebase_id_form_result = ask_for_firebase_id()
        if firebase_id_form_result == -1:
            return
        else:
            firebase_id = firebase_id_form_result

        notification_title_form_result = ask_for_notification_title()
        if notification_title_form_result == -1:
            return
        else:
            if notification_title_form_result:
                title = notification_title_form_result
            else:
                title = "Title :: Test Push"

        notification_body_form_result = ask_for_notification_body()
        if notification_body_form_result == -1:
            return
        else:
            if notification_body_form_result:
                body = notification_body_form_result
            else:
                body = "Body :: Test Push"

        notification_deeplink_form_result = ask_for_notification_deeplink()
        if notification_deeplink_form_result == -1:
            return
        else:
            deeplink = notification_deeplink_form_result

        result = FCM().send_push(
            title=title,
            body=body,
            deeplink=deeplink,
            device_token=firebase_id
        )

        UI().ptext(result)
        UI().psuccess()

    @staticmethod
    def fcm_silent_menu():
        UI().clear()
        UI().pheader(f"FCM")
        UI().pline()
        UI().ptext('<g>Send silent push</g>')

        firebase_id_form_result = ask_for_firebase_id()
        if firebase_id_form_result == -1:
            return
        else:
            firebase_id = firebase_id_form_result

        notification_action = ask_for_notification_action()
        if notification_action == -1:
            return
        else:
            if notification_action:
                action = notification_action
            else:
                action = "TRUSTED_DEVICE"

        result = FCM().send_silent_push(
            action=action,
            device_token=firebase_id
        )

        UI().ptext(result)
        UI().psuccess()

    @staticmethod
    def lokalise_menu():
        UI().clear()
        UI().pheader(f"LOKALISE")
        UI().pline()
        UI().ptext('<g>Scripts</g>')
        result = get_lokalise_menu_form()

        if result == -1:
            return
        else:
            UI().clear()
            UI().psuccess()

    @staticmethod
    def jira_menu():
        UI().clear()
        UI().pheader(f"JIRA")
        UI().pline()
        UI().ptext('<g>Create task</g>')

        issue_type_form_result = get_jira_issue_form()

        if issue_type_form_result == -1:
            return
        else:
            issue_type = issue_type_form_result

        if issue_type == 'START RELEASE':
            release_version_form_result = ask_for_release_version()
            if release_version_form_result == -1:
                return
            else:
                release_version = release_version_form_result

            issues_target_date_form_result = ask_for_release_start_date()
            if issues_target_date_form_result == -1:
                return
            else:
                issues_target_date = issues_target_date_form_result

            result = Jira().create_release_and_add_issues(issues_target_date=issues_target_date, version_name=release_version)
            result = result

        elif issue_type == 'CLOSE RELEASE':
            confirm = confirm_question(message="Update release tickets to LIVE:")
            if confirm == -1 or confirm is False:
                return
            else:
                result = Jira().update_release_tickets_live()
                result = result
        else:
            issue_squad_form_result = get_jira_issue_squad_form()

            if issue_squad_form_result == -1:
                return
            else:
                issue_title_form_result = ask_for_issue_title()

                if issue_title_form_result == -1:
                    return
                else:
                    issue_title = issue_title_form_result
                    issue_squad = issue_squad_form_result
                    issue_description_form_result = ask_for_issue_description()

                    if issue_description_form_result == -1:
                        return
                    else:
                        issue_description = issue_description_form_result

                    result = Jira().create_ticket(project_id=issue_type, title=issue_title, squad=issue_squad,
                                                  description=issue_description)

        UI().ptext(result)

        UI().psuccess()

    @staticmethod
    def git_menu():
        UI().clear()
        UI().pheader(f"GIT")
        UI().pline()
        UI().ptext('<g>Options</g>')

        result = get_git_menu_form()

        if result == -1:
            return

        if result == "BRANCH":
            create_new_branch_from_release_branch()
        else:
            create_new_pull_request()

    @staticmethod
    def code_gen_menu():
        working_directory = os.getcwd()
        UI().clear()
        UI().pheader(f"CODE GENERATION")
        UI().pline()
        UI().ptext(f"│  Working directory:")
        UI().ptext(f"│  {working_directory}")
        if (not (working_directory.endswith("mobile-android"))):
            UI().ptext('│  <y>WARNING:</y> This doesn\'t seem to be the right directory.')
        UI().pline()
        UI().ptext('<g>Options</g>')

        result = get_code_gen_menu_form()
        print(result)
        if result == -1:
            return

        if result == "SCREEN":
            create_new_screen()
        else:
            create_new_module()

    # MAIN MENU ------------------------------------
    def main_menu(self):
        options = [
            ("1", f"BITRISE <gray>Menu</gray>", self.bitrise_menu),
            ("2", f"Git <gray>Menu</gray>", self.git_menu),
            ("3", f"Jira <gray>Menu</gray>", self.jira_menu),
            ("4", f"Lokalise <gray>Menu</gray>", self.lokalise_menu),
            ("5", f"AWS <gray>sign-in</gray> {Aws().session}", Aws().sign_in),
            ("6", f"Code Gen <gray>Menu</gray>", self.code_gen_menu),
            ("7", f"FCM <gray>send push</gray>", self.fcm_menu),
            ("8", f"FCM <gray>send silent push</gray>", self.fcm_silent_menu)
        ]

        menu = UIMenuOptions(
            type="main_menu",
            top=f"{base64.b64decode('PHk+QXN0cm8gQW5kcm9pZCBDTEk8L3k+').decode('utf-8')} │ <gray>{App().version}</gray>",
            options=options
        )

        UIMenu().print_menu(menu)
