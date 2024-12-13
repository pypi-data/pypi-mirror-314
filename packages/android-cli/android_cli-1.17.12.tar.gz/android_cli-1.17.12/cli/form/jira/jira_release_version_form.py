import re

import questionary


def ask_for_release_version():
    try:
        message = f'Add release version (ex. 4.41): '
        title = questionary.unsafe_prompt(
            {
                'type': 'text',
                'name': 'value',
                'message': message,
                'default': '',
                'validate': lambda val: 'Invalid format. Format should be like 4.22, 4.22.1' if not
                validate_version_name(val) else True
            }
        )
        return title['value']
    except KeyboardInterrupt:
        return -1


def validate_version_name(value):
    patter = r'^\d{1,2}\.\d{2}(?:\.\d{1,2})?(?:\s[p|x])?$'

    if re.match(patter, value):
        return True
    else:
        return False
