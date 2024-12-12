import dotenv

from .appsettings import load_app_settings
from .keyvault import resolve_key_vault_secrets

"""
This module holds utilities related to configuration.
"""


def load_dotenv(**kwargs):
    """
    Load env vars from dot end, then resolve app settings and secrets.
    """
    dotenv.load_dotenv(**kwargs)  # load from .env file
    load_app_settings()  # load from Azure Web App settings
    resolve_key_vault_secrets()  # load from Azure Key Vault
