import questionary

from cli.utils.configs import custom_style


def ask_for_issue_description():
    try:
        message = f'Add description (optional):'
        description = questionary.unsafe_prompt(
            {
                'type': 'text',
                'name': 'value',
                'message': message,
                'default': ''
            }
        )
        return description['value']
    except KeyboardInterrupt:
        return -1
