import questionary

from cli.utils.configs import custom_style


def get_jira_issue_squad_form():
    try:
        type_choices = [
            'Account Lifecycle',
            'Savings',
            'Money Transfers',
            'Payment Methods',
            'Cards',
            'Rewards',
            'Payments Processing',
            'Help Center',
            'IT'
        ]
        squad = questionary.unsafe_prompt(
            {
                'type': 'select',
                'name': 'value',
                'message': 'Select the Squad:',
                'choices': type_choices,
                'style': custom_style
            }
        )
        return squad['value']
    except KeyboardInterrupt:
        return -1
