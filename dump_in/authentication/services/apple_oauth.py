import jwt

from dump_in.common.exception.exceptions import AuthenticationFailedException


class AppleLoginFlowService:
    def get_user_info(self, identify_token: str) -> dict:
        try:
            return jwt.decode(identify_token, "", options={"verify_signature": False})

        except jwt.exceptions.DecodeError:
            raise AuthenticationFailedException("Token is invalid")
