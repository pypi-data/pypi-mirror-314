import questionary

from cli.utils.configs import BuildType, custom_style


def get_build_type_form():
    try:
        type_choices = [
            BuildType.RELEASE_QA_TESTS.value,
            BuildType.RELEASE.value,
            BuildType.F_AND_F.value,
            BuildType.PROD_FEATURE_BRANCH.value,
            BuildType.TEST_FEATURE_BRANCH.value,
        ]
        build_type = questionary.unsafe_prompt(
            {
                'type': 'select',
                'name': 'value',
                'message': 'Build Type?',
                'choices': type_choices,
                'style': custom_style
            }
        )
        return build_type['value']
    except KeyboardInterrupt:
        return -1
