import json
from typing import Any, Dict

import requests

from dump_in.common.exception.exceptions import AuthenticationFailedException


class KakaoLoginFlowService:
    KAKAO_USER_INFO_URL = "https://kapi.kakao.com/v2/user/me"

    def get_user_info(self, access_token: str) -> Dict[str, Any]:
        response = requests.get(self.KAKAO_USER_INFO_URL, headers={"Authorization": f"Bearer {access_token}"})

        if response.status_code != 200:
            raise AuthenticationFailedException("Failed to get user info from Kakao.")

        return json.loads(response.text)
