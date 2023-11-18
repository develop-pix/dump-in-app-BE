from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers, status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from dump_in.common.base.serializers import (
    BaseResponseExceptionSerializer,
    BaseResponseSerializer,
    BaseSerializer,
)
from dump_in.common.exception.exceptions import ValidationException
from dump_in.common.response import create_response
from dump_in.users.selectors.users import UserSelector
from dump_in.users.services.users import UserService


class UserDetailAPI(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    class InputSerializer(BaseSerializer):
        nickname = serializers.CharField(max_length=16, required=True)

    class OutputSerializer(BaseSerializer):
        id = serializers.IntegerField()
        email = serializers.EmailField()
        nickname = serializers.CharField()

    @swagger_auto_schema(
        tags=["유저"],
        operation_summary="유저 정보 조회",
        responses={
            status.HTTP_200_OK: BaseResponseSerializer(data_serializer=OutputSerializer),
            status.HTTP_401_UNAUTHORIZED: BaseResponseExceptionSerializer(exception=AuthenticationFailed),
        },
    )
    def get(self, request: Request) -> Response:
        """
        인증된 유저가 자신의 정보를 조회합니다.
        url: /app/api/auth/users/detail
        """
        user_selector = UserSelector()
        user = user_selector.get_user_by_id(request.user.id)
        user_data = self.OutputSerializer(user).data
        return create_response(data=user_data, status_code=status.HTTP_200_OK)

    @swagger_auto_schema(
        tags=["유저"],
        operation_summary="유저 정보 수정",
        responses={
            status.HTTP_200_OK: BaseResponseSerializer(data_serializer=OutputSerializer),
            status.HTTP_400_BAD_REQUEST: BaseResponseExceptionSerializer(exception=ValidationException),
            status.HTTP_401_UNAUTHORIZED: BaseResponseExceptionSerializer(exception=AuthenticationFailed),
        },
        request_body=InputSerializer,
    )
    def put(self, request: Request) -> Response:
        """
        인증된 유저가 자신의 정보를 수정합니다. (닉네임)
        url: /app/api/auth/users/detail
        """
        user_service = UserService()
        input_serializer = self.InputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        user = user_service.get_and_update_user(request.user.id, input_serializer.validated_data["nickname"])
        user_data = self.OutputSerializer(user).data
        return create_response(data=user_data, status_code=status.HTTP_200_OK)

    @swagger_auto_schema(
        tags=["유저"],
        operation_summary="유저 정보 탈퇴",
        responses={
            status.HTTP_204_NO_CONTENT: "",
            status.HTTP_401_UNAUTHORIZED: BaseResponseExceptionSerializer(exception=AuthenticationFailed),
        },
    )
    def delete(self, request: Request) -> Response:
        """
        인증된 유저가 자신의 정보를 탈퇴합니다. (소프트 삭제)
        url: /app/api/auth/users/detail
        """
        user_service = UserService()
        user_service.soft_delete_user(request.user.id)
        return create_response(status_code=status.HTTP_204_NO_CONTENT)
