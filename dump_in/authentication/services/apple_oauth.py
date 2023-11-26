import time
from typing import Any, Dict

import jwt
import requests
from attrs import define
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.urls import reverse_lazy

from dump_in.common.exception.exceptions import AuthenticationFailedException


@define
class AppleLoginCredentials:
    team_id: str
    client_id: str
    key_id: str
    private_key: str


class AppleLoginFlowService:
    API_URI = reverse_lazy("api-auth:apple-login-callback")

    APPLE_URL = "https://appleid.apple.com"
    APPLE_AUTH_URL = "https://appleid.apple.com/auth/authorize"
    APPLE_TOKEN_OBTAIN_URL = "https://appleid.apple.com/auth/token"

    def __init__(self):
        self._credentials = apple_login_get_credentials()

    def _get_redirect_uri(self) -> str:
        domain = settings.BASE_BACKEND_URL
        api_uri = self.API_URI
        redirect_uri = f"{domain}{api_uri}"
        return redirect_uri

    def _generate_client_config(self) -> Dict[str, Any]:
        redirect_uri = self._get_redirect_uri()
        client_id = self._credentials.client_id
        return {
            "redirect_uri": redirect_uri,
            "client_id": client_id,
            "response_type": "code",
            "scope": "name email",
            "response_mode": "form_post",
        }

    def get_authorization_url(self) -> str:
        client_config = self._generate_client_config()
        response = requests.get(self.APPLE_AUTH_URL, params=client_config)

        if response.status_code != 200:
            raise AuthenticationFailedException("Failed to get authorization url from Apple.")

        return response.url

    def _get_client_secret(self) -> str:
        headers = {
            "alg": "ES256",
            "kid": self._credentials.key_id,
        }
        payload = {
            "iss": self._credentials.team_id,
            "iat": time.time(),
            "exp": time.time() + 600,
            "aud": self.APPLE_URL,
            "sub": self._credentials.client_id,
        }
        client_secret = jwt.encode(
            payload=payload,
            key=self._credentials.private_key.replace("\\n", "\n"),
            algorithm="ES256",
            headers=headers,
        )
        return client_secret

    def get_id_token(self, code: str):
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = {
            "client_id": self._credentials.client_id,
            "client_secret": self._get_client_secret(),
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": self._get_redirect_uri(),
        }

        response = requests.post(self.APPLE_TOKEN_OBTAIN_URL, headers=headers, data=data)

        if response.status_code != 200:
            raise AuthenticationFailedException("Failed to get access token from Apple.")

        response_data = response.json()
        id_token = response_data.get("id_token")

        token_decoded = jwt.decode(id_token, "", options={"verify_signature": False})

        return token_decoded


def apple_login_get_credentials() -> AppleLoginCredentials:
    team_id = settings.APPLE_TEAM_ID
    client_id = settings.APPLE_CLIENT_ID
    key_id = settings.APPLE_KEY_ID
    private_key = settings.APPLE_PRIVATE_KEY

    if not team_id:
        raise ImproperlyConfigured("APPLE_TEAM_ID missing in env.")

    if not client_id:
        raise ImproperlyConfigured("APPLE_API_KEY missing in env.")

    if not key_id:
        raise ImproperlyConfigured("APPLE_KEY_ID missing in env.")

    if not private_key:
        raise ImproperlyConfigured("APPLE_PRIVATE_KEY missing in env.")

    credentials = AppleLoginCredentials(
        team_id=team_id,
        client_id=client_id,
        key_id=key_id,
        private_key=private_key,
    )

    return credentials
