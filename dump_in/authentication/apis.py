from datetime import datetime

from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers, status
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.views import TokenRefreshView

from dump_in.authentication.services.apple_oauth import AppleLoginFlowService
from dump_in.authentication.services.auth import AuthService
from dump_in.authentication.services.kakao_oauth import KakaoLoginFlowService
from dump_in.authentication.services.naver_oauth import NaverLoginFlowService
from dump_in.common.base.serializers import BaseResponseSerializer, BaseSerializer
from dump_in.common.response import create_response
from dump_in.users.enums import UserProvider
from dump_in.users.services.users import UserService


class UserJWTRefreshAPI(TokenRefreshView):
    class OutputSerializer(BaseSerializer):
        access_token = serializers.CharField()

    @swagger_auto_schema(
        tags=["인증"],
        operation_summary="인증 토큰 재발급",
        responses={
            status.HTTP_200_OK: BaseResponseSerializer(data_serializer=OutputSerializer),
        },
    )
    def post(self, request: Request) -> Response:
        """
        refresh token을 입력받아 access token을 발급합니다.
        url: /app/api/auth/jwt/refresh
        """
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        token_data = self.OutputSerializer({"access_token": serializer.validated_data["access"]}).data
        return create_response(token_data, status_code=status.HTTP_200_OK)


class KakaoLoginAPI(APIView):
    authentication_classes = ()
    permission_classes = (AllowAny,)

    class InputSerializer(BaseSerializer):
        access_token = serializers.CharField(required=True)
        mobile_token = serializers.CharField(required=False, allow_null=True, default=None)

    class OutputSerializer(BaseSerializer):
        access_token = serializers.CharField()
        refresh_token = serializers.CharField()

    @swagger_auto_schema(
        tags=["인증"],
        operation_summary="카카오 로그인",
        request_body=InputSerializer,
        responses={
            status.HTTP_200_OK: BaseResponseSerializer(data_serializer=OutputSerializer),
        },
    )
    def post(self, request: Request) -> Response:
        """
        카카오 로그인 API 입니다. 카카오에서 전달받은 토큰을 토대로 앱 유저를 생성하고,
        액세스 토큰과 리프레쉬 토큰을 발급합니다.
        url: /app/api/auth/kakao/login
        """
        input_serializer = self.InputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        mobile_token = input_serializer.validated_data.get("mobile_token")
        access_token = input_serializer.validated_data["access_token"]

        # Kakao Login Flow
        kakao_login_flow = KakaoLoginFlowService()
        user_info = kakao_login_flow.get_user_info(access_token=access_token)

        # User Info Parsing
        social_id = user_info["id"]
        nickname = user_info["kakao_account"]["profile"]["nickname"]
        email = user_info["kakao_account"]["email"]
        birthyear = user_info["kakao_account"].get("birthyear")
        birthday = user_info["kakao_account"].get("birthday")
        gender = user_info.get("gender")

        birth = datetime.strptime(birthyear + birthday, "%Y%m%d") if birthyear and birthday else None
        gender = "F" if gender == "female" else "M" if gender == "male" else None

        # Create Social User
        user_service = UserService()
        user = user_service.create_social_user(
            social_id=social_id,
            nickname=nickname,
            email=email,
            birth=birth,
            gender=gender,
            social_provider=UserProvider.KAKAO.value,
            mobile_token=mobile_token,
        )

        # User Authenticate & Generate Token
        auth_service = AuthService()
        auth_service.authenticate_user(username=str(user.username))
        refresh_token, access_token = auth_service.generate_token(user=user)
        token_data = self.OutputSerializer({"access_token": access_token, "refresh_token": refresh_token}).data
        return create_response(data=token_data, status_code=status.HTTP_200_OK)


class NaverLoginAPI(APIView):
    authentication_classes = ()
    permission_classes = (AllowAny,)

    class InputSerializer(BaseSerializer):
        access_token = serializers.CharField(required=True)
        mobile_token = serializers.CharField(required=False, allow_null=True, default=None)

    class OutputSerializer(BaseSerializer):
        access_token = serializers.CharField()
        refresh_token = serializers.CharField()

    @swagger_auto_schema(
        tags=["인증"],
        operation_summary="네이버 로그인",
        request_body=InputSerializer,
        responses={
            status.HTTP_200_OK: BaseResponseSerializer(OutputSerializer),
        },
    )
    def post(self, request: Request) -> Response:
        """
        네이버 로그인 API 입니다. 네이버에서 전달받은 토큰을 토대로 앱 유저를 생성하고,
        액세스 토큰과 리프레쉬 토큰을 발급합니다.
        url: /app/api/auth/naver/login
        """
        input_serializer = self.InputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        access_token = input_serializer.validated_data["access_token"]
        mobile_token = input_serializer.validated_data.get("mobile_token")

        # Naver Login Flow
        naver_login_flow = NaverLoginFlowService()
        user_info = naver_login_flow.get_user_info(access_token=access_token)

        # User Info Parsing
        social_id = user_info["id"]
        nickname = user_info["nickname"]
        email = user_info["email"]
        birthyear = user_info["birthyear"]
        birthday = user_info["birthday"]
        gender = user_info["gender"]

        birth = datetime.strptime(f"{birthyear}-{birthday}", "%Y-%m-%d") if birthyear and birthday else None
        gender = gender if gender else None

        # Create Social User
        user_service = UserService()
        user = user_service.create_social_user(
            social_id=social_id,
            nickname=nickname,
            email=email,
            birth=birth,
            gender=gender,
            social_provider=UserProvider.NAVER.value,
            mobile_token=mobile_token,
        )

        # User Authenticate & Generate Token
        auth_service = AuthService()
        auth_service.authenticate_user(username=str(user.username))
        refresh_token, access_token = auth_service.generate_token(user=user)
        token_data = self.OutputSerializer({"access_token": access_token, "refresh_token": refresh_token}).data
        return create_response(data=token_data, status_code=status.HTTP_200_OK)


class AppleLoginAPI(APIView):
    authentication_classes = ()
    permission_classes = (AllowAny,)

    class InputSerializer(BaseSerializer):
        identify_token = serializers.CharField(required=True)
        mobile_token = serializers.CharField(required=False, allow_null=True, default=None)

    class OutputSerializer(BaseSerializer):
        access_token = serializers.CharField()
        refresh_token = serializers.CharField()

    @swagger_auto_schema(
        tags=["인증"],
        operation_summary="애플 로그인",
        request_body=InputSerializer,
        responses={
            status.HTTP_200_OK: BaseResponseSerializer(OutputSerializer),
        },
    )
    def post(self, request: Request) -> Response:
        """
        애플 로그인 API 입니다. 애플에서 전달받은 토큰을 토대로 앱 유저를 생성하고,
        액세스 토큰과 리프레쉬 토큰을 발급합니다.
        url: /app/api/auth/apple/login
        """
        input_serializer = self.InputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        identify_token = input_serializer.validated_data["identify_token"]
        mobile_token = input_serializer.validated_data.get("mobile_token")

        # Apple Login Flow
        apple_login_flow = AppleLoginFlowService()
        user_info = apple_login_flow.get_user_info(identify_token=identify_token)

        social_id = user_info["sub"]
        email = user_info.get("email", None)

        # Create Social User
        user_service = UserService()
        user = user_service.create_social_user(
            social_id=social_id,
            nickname=None,
            email=email,
            birth=None,
            gender=None,
            social_provider=UserProvider.APPLE.value,
            mobile_token=mobile_token,
        )

        # User Authenticate & Generate Token
        auth_service = AuthService()
        auth_service.authenticate_user(username=str(user.username))
        refresh_token, access_token = auth_service.generate_token(user=user)
        token_data = self.OutputSerializer({"access_token": access_token, "refresh_token": refresh_token}).data
        return create_response(data=token_data, status_code=status.HTTP_200_OK)
