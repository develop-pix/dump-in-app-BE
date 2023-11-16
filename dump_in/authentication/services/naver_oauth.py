import json
from random import SystemRandom
from typing import Any, Dict

import requests
from attrs import define
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.urls import reverse_lazy
from oauthlib.common import UNICODE_ASCII_CHARACTER_SET

from dump_in.common.exception.exceptions import AuthenticationFailedException


@define
class NaverLoginCredentials:
    client_id: str
    client_secret: str


@define
class NaverAccessToken:
    access_token: str


class NaverLoginFlowService:
    API_URI = reverse_lazy("api-auth:naver-login-callback")

    NAVER_AUTH_URL = "https://nid.naver.com/oauth2.0/authorize"
    NAVER_ACCESS_TOKEN_OBTAIN_URL = "https://nid.naver.com/oauth2.0/token"
    NAVER_USER_INFO_URL = "https://openapi.naver.com/v1/nid/me"

    def __init__(self):
        self._credentials = naver_login_get_credentials()

    @staticmethod
    def _generate_state(length=30, chars=UNICODE_ASCII_CHARACTER_SET):
        rand = SystemRandom()
        state = "".join(rand.choice(chars) for _ in range(length))
        return state

    def _get_redirect_uri(self):
        domain = settings.BASE_BACKEND_URL
        api_uri = self.API_URI
        redirect_uri = f"{domain}{api_uri}"
        return redirect_uri

    def _generate_client_config(self):
        redirect_uri = self._get_redirect_uri()
        client_id = self._credentials.client_id
        state = self._generate_state()
        return {"redirect_uri": redirect_uri, "client_id": client_id, "response_type": "code", "state": state}

    def get_authorization_url(self) -> str:
        client_config = self._generate_client_config()
        response = requests.get(self.NAVER_AUTH_URL, params=client_config)

        if response.status_code != 200:
            raise AuthenticationFailedException("Failed to get authorization url from Naver.")
        return response.url

    def get_token(self, code: str, state: str) -> NaverAccessToken:
        data = {
            "grant_type": "authorization_code",
            "client_id": self._credentials.client_id,
            "client_secret": self._credentials.client_secret,
            "code": code,
            "state": state,
        }

        response = requests.post(self.NAVER_ACCESS_TOKEN_OBTAIN_URL, data=data)
        if response.status_code != 200:
            raise AuthenticationFailedException("Failed to get access token from Naver.")

        naver_token = NaverAccessToken(access_token=json.loads(response.text)["access_token"])

        return naver_token

    def get_user_info(self, naver_token: NaverAccessToken) -> Dict[str, Any]:
        access_token = naver_token.access_token
        response = requests.get(self.NAVER_USER_INFO_URL, headers={"Authorization": f"Bearer {access_token}"})

        if response.status_code != 200:
            raise AuthenticationFailedException("Failed to get user info from Naver.")

        return json.loads(response.text)["response"]


def naver_login_get_credentials() -> NaverLoginCredentials:
    client_id = settings.NAVER_CLIENT_ID
    client_secret = settings.NAVER_CLIENT_SECRET

    if not client_id:
        raise ImproperlyConfigured("NAVER_CLIENT_ID missing in env.")

    if not client_secret:
        raise ImproperlyConfigured("NAVER_CLIENT_SECRET missing in env.")

    credentials = NaverLoginCredentials(client_id=client_id, client_secret=client_secret)

    return credentials
