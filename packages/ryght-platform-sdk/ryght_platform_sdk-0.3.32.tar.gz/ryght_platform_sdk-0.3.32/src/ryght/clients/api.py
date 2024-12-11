# -------------------------------------------------------------------------------------------------------------------- #
# <---| * Import section |--->
# -------------------------------------------------------------------------------------------------------------------- #
import time
import logging

from ryght.utils import RequestMethods
from ryght.interface import ModelsAPI
from ryght.interface import DocumentsAPI
from ryght.interface import CompletionsAPI
from ryght.interface import OrganizationAPI
from ryght.interface import ConversationsAPI
from ryght.interface import DocumentCollectionAPI
from ryght.interface import PermissionManagementAPI
from ryght.interface import MedicalCodingAPI

# -------------------------------------------------------------------------------------------------------------------- #
# <---| * Logger Definition |--->
# -------------------------------------------------------------------------------------------------------------------- #
logger = logging.getLogger(__name__)


# -------------------------------------------------------------------------------------------------------------------- #
# <---| * Class Definition |--->
# -------------------------------------------------------------------------------------------------------------------- #
class ApiClient(
    ModelsAPI,
    DocumentsAPI,
    CompletionsAPI,
    OrganizationAPI,
    ConversationsAPI,
    DocumentCollectionAPI,
    PermissionManagementAPI,
    MedicalCodingAPI
):
    pass


# -------------------------------------------------------------------------------------------------------------------- #
class ApiProxyClient(
    ModelsAPI,
    DocumentsAPI,
    CompletionsAPI,
    OrganizationAPI,
    ConversationsAPI,
    DocumentCollectionAPI,
    PermissionManagementAPI,
    MedicalCodingAPI
):
    def __init__(
            self,
            /,
            token_str: str,
            *,
            env: str,
            token_type: str = 'Bearer',

    ):
        super().__init__(env=env)
        self.access_token = token_str
        self.token_type = token_type

    @property
    def authorization_param(self) -> str:
        return (lambda: self.token_type + ' ' + self.access_token)()

    def get_headers(self):
        return {'Authorization': self.authorization_param}

    def execute_request(
            self,
            method: RequestMethods,
            url,
            **kwargs
    ) -> dict | str:

        try:
            match method:
                case RequestMethods.GET:
                    request_fn = self.http_request_exec.get
                case RequestMethods.PUT:
                    request_fn = self.http_request_exec.put
                case RequestMethods.POST:
                    request_fn = self.http_request_exec.post
                case RequestMethods.PATCH:
                    request_fn = self.http_request_exec.patch
                case RequestMethods.DELETE:
                    request_fn = self.http_request_exec.delete
                case _:
                    raise ValueError(f'Unknown method {method}')

            response = request_fn(url=url, **kwargs)

            match response.status_code:
                case 200 | 201 | 202 | 203 | 204:
                    if response.headers.get('Content-Type') == 'application/json':
                        return response.json()
                    elif response.text is not None and response.text != '':
                        value = response.text
                        return f'Success! response text: {value}'
                    else:
                        return f'Success! response code: {response.status_code}'

                case 400 | 402 | 403 | 404:
                    logger.error(
                        f'Got client error: {response.status_code}, '
                        f'Please check your credential & api endpoint variables'
                    )
                    response.raise_for_status()

                case 500 | 502 | 503 | 504:
                    logger.error('Got client error: 500, attempting new token request after 5 seconds')
                    time.sleep(5)
                    # try this outside this func
                    response = request_fn(url=url, **kwargs)
                    response.raise_for_status()

                case _:
                    logger.error(f'Unknown response status code: {response.status_code}')
        except ValueError as value_error:
            logger.error(f'ValueError occurred: {value_error}')
        except Exception as exception:
            logger.error('Exception occurred: {}'.format(exception))

# -------------------------------------------------------------------------------------------------------------------- #
