import questionary

from cli.utils.configs import custom_style


def ask_for_issue_title():
    try:
        message = f'Add title:'
        title = questionary.unsafe_prompt(
            {
                'type': 'text',
                'name': 'value',
                'message': message,
                'default': '',
                'validate': lambda val: 'Title cannot be empty' if not validate_title(
                    val) else True
            }
        )
        return title['value']
    except KeyboardInterrupt:
        return -1


def validate_title(value):
    if value:
        return True
    else:
        return False
