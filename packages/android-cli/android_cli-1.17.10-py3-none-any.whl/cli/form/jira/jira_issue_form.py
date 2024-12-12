import questionary

from cli.utils.configs import custom_style


def get_jira_issue_form():
    try:
        type_choices = [
            'NPR',
            'BUG',
            'START RELEASE',
            'CLOSE RELEASE'
        ]
        issue_type = questionary.unsafe_prompt(
            {
                'type': 'select',
                'name': 'value',
                'message': 'Select the type of task to create:',
                'choices': type_choices,
                'style': custom_style
            }
        )
        return issue_type['value']
    except KeyboardInterrupt:
        return -1
