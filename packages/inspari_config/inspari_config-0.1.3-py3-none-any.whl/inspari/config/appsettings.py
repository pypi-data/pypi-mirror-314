import os


"""
This module holds parsing logic for Azure Web App settings.
"""


_appsettings_prefix = "APPSETTING_"


def load_app_settings():
    """
    Application settings in Azure are prefixed by "APPSETTING_". This function removes the prefix thereby
    making the settings available to the application on equal footing with other environment variables.
    """
    for key in os.environ:
        load_app_setting(key)


def load_app_setting(key: str):
    if key.startswith(_appsettings_prefix):
        os.environ[key.replace(_appsettings_prefix, "")] = os.environ[key]
