import os
import subprocess
from cli.entities.setting import Settings
from cli.utils.singleton import singleton
import questionary


@singleton
class App:
    version: str = "1.17.8"

    def init(self):
        os.system('printf "\033c"')
        os.system('cls' if os.name == 'nt' else 'clear')

        print(f"Press [enter] to start GIT-CLI {self.version}")

        # await Aws().check_session()
        Settings().init()
        self.init_install()

    @staticmethod
    def close():
        os.system('printf "\033c"')
        os.system('cls' if os.name == 'nt' else 'clear')
        exit()

    def init_install(self):
        aws_profile = Settings().config['aws_profile']
        jira_email = Settings().config['jira']['user']
        jira_token = Settings().config['jira']['token']
        lokalise_api_token = Settings().config['lokalise']['api_token']
        lokalise_project_id = Settings().config['lokalise']['project_id']
        bitrise_test_token = Settings().config['bitrise']['test']['build_trigger_token']
        bitrise_prod_token = Settings().config['bitrise']['prod']['build_trigger_token']

        try:
            subprocess.run(['git', 'config', '--global', '--unset-all', 'core.editor'], check=True, stdout=True,
                           stderr=True)
        except:
            pass

        try:
            subprocess.run(['git', 'config', '--global', 'core.editor', 'none'], check=True,
                           stdout=True, stderr=True)
        except subprocess.CalledProcessError as e:
            print(e)
            print("Hubo un error al establecer el editor en Git.")

        if aws_profile == '' or aws_profile is None or aws_profile == 'username':
            try:
                input_aws_profile = questionary.unsafe_prompt([
                    {
                        'type': 'input',
                        'name': 'aws_profile',
                        'message': f'AWS Profile: ',
                    }])

                Settings().config['aws_profile'] = input_aws_profile['aws_profile']
                Settings().save()

            except KeyboardInterrupt:
                self.close()

        if jira_email == '' or jira_email is None or jira_email == 'username':
            try:
                input_jira_token = questionary.unsafe_prompt([
                    {
                        'type': 'input',
                        'name': 'jira_email',
                        'message': f'Jira user: (ex: pepe@astropay.com)'
                    }])

                Settings().config['jira']['user'] = input_jira_token['jira_email']
                Settings().save()

            except KeyboardInterrupt:
                self.close()

        if jira_token == '' or jira_token is None or jira_token == 'token':
            try:
                input_jira_token = questionary.unsafe_prompt([
                    {
                        'type': 'input',
                        'name': 'jira_token',
                        'message': f'Jira token: '
                    }])

                Settings().config['jira']['token'] = input_jira_token['jira_token']
                Settings().save()

            except KeyboardInterrupt:
                self.close()

        if lokalise_api_token == '' or lokalise_api_token is None or lokalise_api_token == 'api_token':
            try:
                input_lokalise_api_token = questionary.unsafe_prompt([
                    {
                        'type': 'input',
                        'name': 'api_token',
                        'message': f'Lokalise api token: '
                    }])

                Settings().config['lokalise']['api_token'] = input_lokalise_api_token['api_token']
                Settings().save()

            except KeyboardInterrupt:
                self.close()

        if lokalise_project_id == '' or lokalise_project_id is None or lokalise_project_id == 'project_id':
            try:
                input_lokalise_project_id = questionary.unsafe_prompt([
                    {
                        'type': 'input',
                        'name': 'project_id',
                        'message': f'Lokalise project id: '
                    }])

                Settings().config['lokalise']['project_id'] = input_lokalise_project_id['project_id']
                Settings().save()

            except KeyboardInterrupt:
                self.close()

        if bitrise_test_token == '' or bitrise_test_token is None:
            try:
                input_bitrise_test_token = questionary.unsafe_prompt([
                    {
                        'type': 'input',
                        'name': 'token',
                        'message': f'[TEST] Bitrise token: '
                    }])

                input_bitrise_test_id = questionary.unsafe_prompt([
                    {
                        'type': 'input',
                        'name': 'id',
                        'message': f'[TEST] Bitrise project id: '
                    }])

                Settings().config['bitrise']['test']['build_trigger_token'] = input_bitrise_test_token['token']
                Settings().config['bitrise']['test']['curl_url_id'] = input_bitrise_test_id['id']
                Settings().save()

            except KeyboardInterrupt:
                self.close()

        if bitrise_prod_token == '' or bitrise_prod_token is None:
            try:
                input_bitrise_prod_token = questionary.unsafe_prompt([
                    {
                        'type': 'input',
                        'name': 'token',
                        'message': f'[PROD] Bitrise token: '
                    }])

                input_bitrise_prod_id = questionary.unsafe_prompt([
                    {
                        'type': 'input',
                        'name': 'id',
                        'message': f'[PROD] Bitrise project id: '
                    }])

                Settings().config['bitrise']['prod']['build_trigger_token'] = input_bitrise_prod_token['token']
                Settings().config['bitrise']['prod']['curl_url_id'] = input_bitrise_prod_id['id']
                Settings().save()

            except KeyboardInterrupt:
                self.close()
