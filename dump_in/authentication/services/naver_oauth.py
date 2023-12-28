import json
from typing import Any, Dict

import requests

from dump_in.common.exception.exceptions import AuthenticationFailedException


class NaverLoginFlowService:
    NAVER_USER_INFO_URL = "https://openapi.naver.com/v1/nid/me"

    def get_user_info(self, access_token: str) -> Dict[str, Any]:
        response = requests.get(self.NAVER_USER_INFO_URL, headers={"Authorization": f"Bearer {access_token}"})

        if response.status_code != 200:
            raise AuthenticationFailedException("Failed to get user info from Naver.")

        return json.loads(response.text)["response"]
