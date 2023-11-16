from datetime import datetime

from django.shortcuts import redirect
from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from dump_in.authentication.services.auth import AuthService, RefreshTokenAuthentication
from dump_in.authentication.services.kakao_oauth import KakaoLoginFlowService
from dump_in.authentication.services.naver_oauth import NaverLoginFlowService
from dump_in.common.base.serializers import BaseResponseSerializer, BaseSerializer
from dump_in.common.enums import UserProvider
from dump_in.common.exception.exceptions import AuthenticationFailedException
from dump_in.common.response import create_response
from dump_in.users.services.users import UserService


class UserJWTRefreshAPI(APIView):
    authentication_classes = (RefreshTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    class OutputSerializer(BaseSerializer):
        access_token = serializers.CharField()

    @swagger_auto_schema(
        tags=["인증"],
        operation_summary="인증 토큰 재발급",
        responses={
            status.HTTP_200_OK: BaseResponseSerializer(data_serializer=OutputSerializer),
        },
    )
    def get(self, request: Request) -> Response:
        """
        refresh token을 입력받아 access token을 발급합니다.
        url: /api/auth/jwt/refresh
        """
        auth_service = AuthService()
        access_token = auth_service.generate_access_token(request.auth)
        access_token_data = self.OutputSerializer({"access_token": access_token}).data
        return create_response(data=access_token_data, status_code=status.HTTP_200_OK)


class KakaoLoginRedirectAPI(APIView):
    authentication_classes = ()
    permission_classes = (AllowAny,)

    @swagger_auto_schema(
        tags=["인증"],
        operation_summary="카카오 로그인 리다이렉트",
    )
    def get(self, request: Request):
        """
        카카오 로그인을 위한 리다이렉트 URL로 이동합니다.
        url: /api/auth/kakao/redirect
        """
        kaka_login_flow = KakaoLoginFlowService()
        authorization_url = kaka_login_flow.get_authorization_url()
        return redirect(authorization_url)


class KakaoLoginAPI(APIView):
    authentication_classes = ()
    permission_classes = (AllowAny,)

    class InputSerializer(BaseSerializer):
        code = serializers.CharField(required=False)
        error = serializers.CharField(required=False)

    class OutputSerializer(BaseSerializer):
        access_token = serializers.CharField()

    @swagger_auto_schema(
        tags=["인증"],
        operation_summary="카카오 로그인 콜백",
        query_serializer=InputSerializer,
        responses={
            status.HTTP_200_OK: BaseResponseSerializer(data_serializer=OutputSerializer),
        },
    )
    def get(self, request: Request) -> Response:
        """
        카카오 로그인 콜백 API 입니다. 카카오 로그인을 완료하면, 카카오에서 전달받은 정보를 토대로
        앱 유저를 생성하고, 액세스 토큰을 발급하고 리프레쉬 토큰은 쿠키에 저장합니다.
        url: /api/auth/kakao/callback
        """
        input_serializer = self.InputSerializer(data=request.GET)
        input_serializer.is_valid(raise_exception=True)
        validated_data = input_serializer.validated_data
        code = validated_data.get("code")
        error = validated_data.get("error")

        if error is not None:
            raise AuthenticationFailedException(error)

        if code is None:
            raise AuthenticationFailedException("Code is not provided")

        # Kakao Login Flow
        kakao_login_flow = KakaoLoginFlowService()
        kakao_token = kakao_login_flow.get_token(code=code)
        user_info = kakao_login_flow.get_user_info(kakao_token=kakao_token)

        # User Info Parsing
        birthyear = user_info["kakao_account"].get("birthyear")
        birthday = user_info["kakao_account"].get("birthday")
        gender = user_info.get("gender")

        birth = datetime.strptime(birthyear + birthday, "%Y%m%d") if birthyear and birthday else None
        gender = "F" if gender == "female" else "M" if gender == "male" else None

        # Create Social User
        user_service = UserService()
        user = user_service.get_or_create_social_user(
            social_id=user_info["id"],
            nickname=user_info["kakao_account"]["profile"]["nickname"],
            email=user_info["kakao_account"]["email"],
            birth=birth,
            gender=gender,
            social_provider=UserProvider.KAKAO.value,
        )

        # User Authenticate & Generate Token
        auth_service = AuthService()
        auth_service.authenticate_user(str(user.username))
        refresh_token, access_token = auth_service.generate_token(user)
        access_token_data = self.OutputSerializer({"access_token": access_token}).data
        response = create_response(data=access_token_data, status_code=status.HTTP_200_OK)
        auth_service.set_refresh_token_cookie(response, refresh_token)
        return response


class NaverLoginRedirectApi(APIView):
    authentication_classes = ()
    permission_classes = (AllowAny,)

    @swagger_auto_schema(
        tags=["인증"],
        operation_summary="네이버 로그인 리다이렉트",
    )
    def get(self, request: Request):
        """
        네이버 로그인을 위한 리다이렉트 URL로 이동합니다.
        url: /api/auth/naver/redirect
        """
        naver_login_flow = NaverLoginFlowService()
        authorization_url = naver_login_flow.get_authorization_url()
        return redirect(authorization_url)


class NaverLoginApi(APIView):
    permission_classes = (AllowAny,)
    authentication_classes = ()

    class InputSerializer(BaseSerializer):
        code = serializers.CharField(required=False)
        error = serializers.CharField(required=False)
        state = serializers.CharField(required=False)

    class OutputSerializer(BaseSerializer):
        access_token = serializers.CharField()

    @swagger_auto_schema(
        tags=["인증"],
        operation_summary="네이버 로그인 콜백",
        query_serializer=InputSerializer,
        responses={
            status.HTTP_200_OK: BaseResponseSerializer(OutputSerializer),
        },
    )
    def get(self, request: Request) -> Response:
        """
        네이버 로그인 콜백 API 입니다. 네이버 로그인을 완료하면, 네이버에서 전달받은 정보를 토대로
        앱 유저를 생성하고, 액세스 토큰을 발급하고 리프레쉬 토큰은 쿠키에 저장합니다.
        url: /api/auth/naver/callback
        """
        input_serializer = self.InputSerializer(data=request.GET)
        input_serializer.is_valid(raise_exception=True)
        validated_data = input_serializer.validated_data

        code = validated_data.get("code")
        error = validated_data.get("error")
        state = validated_data.get("state")

        if error is not None:
            raise AuthenticationFailedException(error)

        if code is None or state is None:
            raise AuthenticationFailedException("Code and State is not provided")

        # Naver Login Flow
        naver_login_flow = NaverLoginFlowService()
        naver_token = naver_login_flow.get_token(code=code, state=state)
        user_info = naver_login_flow.get_user_info(naver_token=naver_token)

        # User Info Parsing
        birthyear = user_info["birthyear"]
        birthday = user_info["birthday"]
        gender = user_info["gender"]

        birth = datetime.strptime(f"{birthyear}-{birthday}", "%Y-%m-%d") if birthyear and birthday else None
        gender = gender if gender else None

        # Create Social User
        user_service = UserService()
        user = user_service.get_or_create_social_user(
            social_id=user_info["id"],
            nickname=user_info["nickname"],
            email=user_info["email"],
            birth=birth,
            gender=gender,
            social_provider=UserProvider.NAVER.value,
        )

        # User Authenticate & Generate Token
        auth_service = AuthService()
        auth_service.authenticate_user(str(user.username))
        refresh_token, access_token = auth_service.generate_token(user)
        access_token_data = self.OutputSerializer({"access_token": access_token}).data
        response = create_response(data=access_token_data, status_code=status.HTTP_200_OK)
        auth_service.set_refresh_token_cookie(response, refresh_token)
        return response
