from enum import Enum

from prompt_toolkit.styles import Style


class BuildType(Enum):
    RELEASE_QA_TESTS = "RELEASE_QA_TESTS"
    RELEASE = "RELEASE"
    F_AND_F = "F&F"
    PROD_FEATURE_BRANCH = "PROD_FEATURE_BRANCH"
    TEST_FEATURE_BRANCH = "TEST_FEATURE_BRANCH"

    @staticmethod
    def from_string(s):
        for build_type in BuildType:
            if build_type.value == s:
                return build_type
        raise ValueError(f"BuildType '{s}' unknown.")


custom_style = Style([
    ('qmark', 'fg:#673ab7 bold'),  # Color y estilo para el símbolo de la pregunta
    ('question', 'bold'),  # Estilo para la pregunta
    ('selected', 'fg:#cc5454 bold'),  # Color para la opción seleccionada
    ('pointer', 'fg:#673ab7 bold'),  # Color y estilo para el puntero
    ('highlighted', 'fg:#2ecc71 bold'),  # Color y estilo para la opción destacada
    # ('answer', 'fg:#f44336 bold'),  # Color y estilo para la respuesta
    ('text', ''),  # Estilo para el texto normal
])
