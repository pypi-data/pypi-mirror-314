import re
from datetime import datetime

import questionary


def ask_for_release_start_date():
    try:
        message = f'Add start date (YYYY-MM-DD): '
        date = questionary.unsafe_prompt(
            {
                'type': 'text',
                'name': 'value',
                'message': message,
                'default': '',
                'validate': lambda val: 'Invalid format. Format should be like 2024-02-14 (YYYY-MM-DD)' if not
                validate_date_format(val) else True
            }
        )
        return date['value']
    except KeyboardInterrupt:
        return -1


def validate_date_format(value):
    date_format = "%Y-%m-%d"
    try:
        datetime.strptime(value, date_format)
        return True
    except ValueError:
        return False
