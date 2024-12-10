from setuptools import setup, find_packages

setup(
    name="android-cli",
    version="1.17.9",
    packages=find_packages(),
    install_requires=[
        "questionary",
        "requests",
        "python-lokalise-api",
        "prompt_toolkit",
        "google-cloud-firestore",
        "google-auth"
        # "curio"
    ],
    entry_points={
        'console_scripts': [
            'dev.cli=cli.main:main_function',
        ],
    },
)
