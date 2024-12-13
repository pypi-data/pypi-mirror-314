import os
import re

import questionary

from cli.utils.configs import BuildType, custom_style


def extract_version_name():
    current_dir = os.getcwd()
    file = f"{current_dir}/buildSrc/src/main/kotlin/android-config.gradle.kts"
    try:
        with open(file, 'r') as file:
            content = file.read()
            patron_version_name = r"versionName\s*=\s*\"([^\"]+)\""
            version_name_match = re.search(patron_version_name, content)
            version_name = version_name_match.group(1) if version_name_match else None

            return version_name
    except FileNotFoundError:
        return False
    except IOError as e:
        return False


def get_version_name_form(build_type: BuildType):
    version_name = extract_version_name()

    if version_name:
        if build_type == BuildType.PROD_FEATURE_BRANCH or build_type == BuildType.TEST_FEATURE_BRANCH:
            return version_name
        else:
            try:
                choices = ["Yes", "No"]
                message = f"Is {version_name} the correct version name?"
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
                    return version_name
                else:
                    return ask_for_version_name()
            except KeyboardInterrupt:
                return -1
    else:
        return ask_for_version_name()


def ask_for_version_name():
    try:
        version_name = questionary.unsafe_prompt(
            {
                'type': 'text',
                'name': 'value',
                'message': 'Which is the versionName?',
                'default': '',
                'validate': lambda val: 'Invalid format. Format should be like 4.22, 4.22.1' if not
                validate_version_name(val) else True
            }
        )
        return version_name['value']
    except KeyboardInterrupt:
        return -1


def validate_version_name(value):
    patter = r'^\d{1,2}\.\d{2}(?:\.\d{1,2})?(?:\s[p|x])?$'

    if re.match(patter, value):
        return True
    else:
        return False
