# <---| * Module Information |--->
# ==================================================================================================================== #
"""
    :param FileName     :   http_requestor.py
    :param Author       :   Sudo
    :param Date         :   2/12/2024
    :param Copyright    :   Copyright (c) 2024 Ryght, Inc. All Rights Reserved.
    :param License      :   #
    :param Description  :   #
"""
__author__ = 'Data engineering team'
__copyright__ = 'Copyright (c) 2024 Ryght, Inc. All Rights Reserved.'

# -------------------------------------------------------------------------------------------------------------------- #
# <---| * Import section |--->
# -------------------------------------------------------------------------------------------------------------------- #
import httpx
import logging
import functools

from result import Result, Ok, Err, is_err, is_ok

# -------------------------------------------------------------------------------------------------------------------- #
# <---| * Logger Definition |--->
# -------------------------------------------------------------------------------------------------------------------- #
logger = logging.getLogger(__name__)


# -------------------------------------------------------------------------------------------------------------------- #
# <---| * Class Definition |--->
# -------------------------------------------------------------------------------------------------------------------- #

class HttpxRequestExecutor:
    def __init__(self):
        self.client = httpx.Client()

    @staticmethod
    def handle_errors(func):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            try:
                response = func(self, *args, **kwargs)
                return response
            except httpx.RequestError as e:
                logger.error(f"An error occurred while requesting {e.request.url!r}")
            except httpx.HTTPStatusError as e:
                logger.error(f"Error response {e.response.status_code} while requesting {e.request.url!r}.")
            except Exception as e:
                logger.error(f"An unexpected error occurred: {e}")
        return wrapper

    @handle_errors
    def get(self, url, **kwargs):
        return self.client.get(url, **kwargs)

    @handle_errors
    def post(self, url, data=None, **kwargs):
        return self.client.post(url, data=data, **kwargs)

    @handle_errors
    def put(self, url, data=None, **kwargs):
        return self.client.put(url, data=data, **kwargs)

    @handle_errors
    def patch(self, url, **kwargs):
        return self.client.patch(url, **kwargs)

    @handle_errors
    def delete(self, url, **kwargs):
        return self.client.delete(url, **kwargs)

    def close(self):
        logger.debug('Closing Httpx client Session ...')
        self.client.close()
        logger.debug('Httpx client session closed...')

    def __del__(self):
        self.close()
# -------------------------------------------------------------------------------------------------------------------- #
