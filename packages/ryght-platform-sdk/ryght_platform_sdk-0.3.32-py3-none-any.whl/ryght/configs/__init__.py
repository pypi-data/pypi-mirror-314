# -------------------------------------------------------------------------------------------------------------------- #
# <---| * Import section |--->
# -------------------------------------------------------------------------------------------------------------------- #
import os

from .api_config import ApiEndpoints
from pydantic_settings import BaseSettings, SettingsConfigDict


# -------------------------------------------------------------------------------------------------------------------- #
# <---| * Class Definition |--->
# -------------------------------------------------------------------------------------------------------------------- #
class Credentials(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env.prod', env_file_encoding='utf-8', extra='ignore')

    username: str | None
    password: str | None
    client_id: str | None
    organization: str | None
    client_secret: str | None

    @staticmethod
    def init_none():
        return Credentials(**{
            'username': None,
            'password': None,
            'client_id': None,
            'client_secret': None,
            'organization': None
        })

    @staticmethod
    def from_environment_variables():
        """

        :return: Credentials
        """
        username = os.getenv('RYGHT_USERNAME', 'No Username found')
        password = os.getenv('RYGHT_PASSWORD', 'No Password found')
        client_id = os.getenv('RYGHT_CLIENT_ID', 'No client id found')
        client_secret = os.getenv('RYGHT_CLIENT_SECRET', 'No client secret found')
        organization = os.getenv('RYGHT_ORGANIZATION', 'No organization found')

        return Credentials(**{
            'username': username,
            'password': password,
            'client_id': client_id,
            'client_secret': client_secret,
            'organization': organization,

        })

# -------------------------------------------------------------------------------------------------------------------- #
