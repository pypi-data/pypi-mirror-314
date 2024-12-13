import os
import random
import re

import questionary

from cli.utils.configs import BuildType, custom_style


def extract_version_code():
    current_dir = os.getcwd()
    file = f"{current_dir}/buildSrc/src/main/kotlin/android-config.gradle.kts"
    try:
        with open(file, 'r') as file:
            content = file.read()
            patron_version_code = r"versionCode\s*=\s*(\d+)"
            version_code_match = re.search(patron_version_code, content)
            version_code = version_code_match.group(1) if version_code_match else False

            return version_code
    except FileNotFoundError:
        return False
    except IOError as e:
        return False






def sum_random_number(number):
    number = int(number)
    random_number = random.randint(301, 400)
    result = number + random_number
    return str(result)


def get_version_code_form(build_type: BuildType):
    version_code = extract_version_code()

    if version_code:
        if build_type == BuildType.PROD_FEATURE_BRANCH or build_type == BuildType.TEST_FEATURE_BRANCH:
            return sum_random_number(version_code)
        else:
            try:
                choices = ["Yes", "No"]
                message = f"Is {version_code} the correct versionCode?"
                response = questionary.unsafe_prompt(
                    {
                        'type': 'select',
                        'name': 'value',
                        'message': message,
                        'choices': choices,
                        'style': custom_style
                    }
                )
                if response['value'] == "Yes":
                    return version_code
                else:
                    return ask_for_version_code()
            except KeyboardInterrupt:
                return -1
    else:
        return ask_for_version_code()


def ask_for_version_code():
    try:
        message = f'Which is the versionCode?'
        version_code = questionary.unsafe_prompt(
            {
                'type': 'text',
                'name': 'value',
                'message': message,
                'default': '',
                'validate': lambda val: 'Invalid format. Format should be like 512, 513' if not
                validate_version_code(val) else True
            }
        )
        return version_code['value']
    except KeyboardInterrupt:
        return -1


def validate_version_code(value):
    if value and value.isdigit() and int(value) > 500:
        return True
    else:
        return False
