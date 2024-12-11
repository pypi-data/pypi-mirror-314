# <---| * Module Information |--->
# ==================================================================================================================== #
"""
    :param FileName     :   tokens.py
    :param Author       :   Sudo
    :param Date         :   2/02/2024
    :param Copyright    :   Copyright (c) 2024 Ryght, Inc. All Rights Reserved.
    :param License      :   # TODO
    :param Description  :   # TODO
"""
__author__ = 'Data engineering team'
__copyright__ = 'Copyright (c) 2024 Ryght, Inc. All Rights Reserved.'

# -------------------------------------------------------------------------------------------------------------------- #
# <---| * Import section |--->
# -------------------------------------------------------------------------------------------------------------------- #
import time
import logging
import functools

from threading import Thread
from datetime import datetime
from urllib.parse import urlparse

from ryght.models import Token
from ryght.configs import Credentials
from ryght.requests import HttpxRequestExecutor

# -------------------------------------------------------------------------------------------------------------------- #
# <---| * Logger Definition |--->
# -------------------------------------------------------------------------------------------------------------------- #
logger = logging.getLogger(__name__)


# -------------------------------------------------------------------------------------------------------------------- #
# <---| * Class Definition |--->
# -------------------------------------------------------------------------------------------------------------------- #

class TokenManagerBase:
    """

    """
    token: Token
    credentials: Credentials
    enable_token_watchdog: bool = False
    request_handler: HttpxRequestExecutor

    def __init__(self, token: Token, credentials: Credentials, auth_url: str):
        self.auth_url = auth_url
        self.token = token
        self.credentials = credentials
        self.refresh_interval = 5
        self.headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

    @staticmethod
    def _calculate_time_delta(target: datetime) -> float:
        """
        Calculate the time delta between two datetime objects and return it in seconds
        :param target: datetime object
            Time to calculate time delta from now
        :return: float
            :returns the time delta in seconds
        """
        delta = target - datetime.utcnow()
        return delta.total_seconds()

    def is_access_token_valid(self) -> bool:
        return True if self._calculate_time_delta(self.token.token_expiry) >= 10 else False

    def is_refresh_token_valid(self) -> bool:
        return True if self._calculate_time_delta(self.token.token_expiry) >= 10 else False

    def validate_url(self) -> bool:
        result = urlparse(self.auth_url)
        return all([result.scheme, result.netloc])

    def request_token(
            self,
            payload
    ) -> None:
        try:
            if not self.validate_url():
                raise ValueError(f'URL is not valid')
            logger.info('Initialing Token Request/ refresh')

            response = self.request_handler.post(
                url=self.auth_url,
                headers=self.headers,
                data=payload
            )
            if response.status_code >= 500:
                logger.info('Got client Error: 500, attempting new Token request after 5 seconds')
                time.sleep(5)
                response = self.request_handler.post(
                    url=self.auth_url,
                    headers=self.headers,
                    data=payload
                )
                response.raise_for_status()
            elif response.status_code in [401, 400, 404]:
                logger.info('Got client Error: 401, Please check your credential & api endpoint variables')
                response.raise_for_status()

            if response.status_code == 200:
                self.token = Token(**response.json())
                self.refresh_interval = self.token.expires_in
                logger.info('Successfully updated the token')
            else:
                raise Exception('Error updating token')
        except ValueError as VE:
            logger.info(VE)
        except Exception as E:
            logger.info(E)


# -------------------------------------------------------------------------------------------------------------------- #
class TokenManager(TokenManagerBase):
    """

    """

    def __init__(self, token: Token, credentials: Credentials, requestor: HttpxRequestExecutor, auth_url):
        super().__init__(token, credentials, auth_url)
        self.request_handler: HttpxRequestExecutor = requestor

    @staticmethod
    def authenticate(func):
        """
        Provides authentication logic for API calls and wraps around the target function, such that, before target
        function is called, it will start with authentication and updates the token information before calling the
        appropriate APIs

        :param func: func
            The func to be decorated with authentication logic before calling that target func
        :return: Any
            Returns the same func or the func's return value if authentication succeeds
        """

        @functools.wraps(func)
        def executor(*args, **kwargs):
            logger.info(f'Performing Authentication for {func.__name__} fn call')
            obj = args[0]
            logger.info('Checking access token validity')
            if not obj.token_manager.is_access_token_valid():
                logger.info('Access token Expired, Checking Validity of refresh token')
                if obj.token_manager.is_refresh_token_valid():
                    obj.token_manager.refresh_access_token()
                else:
                    obj.token_manager.get_new_token()
            else:
                logger.info(f'Access token is valid, performing {func.__name__} fn call')

            return func(*args, **kwargs)

        return executor

    def get_new_token(self, organization: str = None) -> None:
        payload: dict = self.credentials.model_dump()
        payload['grant_type'] = 'password'
        if payload.get('organization') is None and organization is not None:
            payload['organization'] = organization
        elif payload.get('organization') is None and organization is None:
            del payload['organization']  # remove field org if it's not set to begin with
        elif payload.get('organization') is not None and organization is not None:
            payload['organization'] = organization
        logger.info('Requesting new token')
        self.request_token(payload=payload)

    def refresh_access_token(self) -> None:
        if self.token.refresh_token:
            payload = {
                'grant_type': 'refresh_token',
                'refresh_token': self.token.refresh_token,
                'client_id': self.credentials.client_id,
                'client_secret': self.credentials.client_secret

            }
            logger.info('refreshing access token, initialing refresh token request')
            self.request_token(payload=payload)
        else:
            self.get_new_token()

    def start_watchdog(self):
        while self.enable_token_watchdog:
            logger.info('Auto-Refreshing Token from Daemon thread')
            self.refresh_access_token()
            time.sleep(self.refresh_interval)
        logger.info('Exiting token auto refresh')

    def enable_token_auto_refresh(self) -> None:
        if not self.enable_token_watchdog:
            self.enable_token_watchdog = True
            thread = Thread(target=self.start_watchdog)
            thread.daemon = True
            thread.start()
            logger.info(f'Started Watch dog for auto refresh in a daemon thread')
        else:
            logger.info('Watch dog is already enabled, if you face issue, disable token auto-refresh and enable again')

    def disable_token_auto_refresh(self) -> None:
        self.enable_token_watchdog = False
        logger.info('Triggering Token Auto Refresh disable sequence')

# -------------------------------------------------------------------------------------------------------------------- #
