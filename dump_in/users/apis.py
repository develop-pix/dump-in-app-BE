# from drf_yasg.utils import swagger_auto_schema
# from rest_framework import serializers, status
# from rest_framework.request import Request
# from rest_framework.response import Response
# from rest_framework.views import APIView

# from dump_in.authentication.mixins import JWTAPTAuthMixin, RefreshTokenAPIAuthMixin
# from dump_in.authentication.services.auth import AuthServices
# from dump_in.common.base.serializers import BaseResponseSerializer, BaseSerializer
# from dump_in.common.response import create_response
# from dump_in.common.utils import inline_serializer
# from dump_in.users.selectors.users import UserSelector


# class UserDetailAPI(RefreshTokenAPIAuthMixin, APIView):
#     class OutputSerializer(BaseSerializer):
#         id = serializers.IntegerField()
#         email = serializers.EmailField()
#         nickname = serializers.CharField()

#     @swagger_auto_schema(
#         tags=["유저"],
#         operation_summary="유저 정보 조회",
#         responses={
#             status.HTTP_200_OK: BaseResponseSerializer(data_serializer=OutputSerializer),
#         },
#     )
#     def get(self, request: Request) -> Response:
#         """
#         refresh token을 입력받아 access token을 발급합니다.
#         url: /api/auth/jwt/refresh
#         """
#         auth_service = AuthServices()
#         access_token = auth_service.generate_access_token(request.auth)
#         access_token_data = self.OutputSerializer({"access_token": access_token}).data
#         return create_response(data=access_token_data, status_code=status.HTTP_200_OK)

#     @swagger_auto_schema(
#         tags=["유저"],
#         operation_summary="유저 정보 수정",
#         responses={
#             status.HTTP_200_OK: BaseResponseSerializer(data_serializer=OutputSerializer),
#         },
#     )
#     def put(self, request: Request) -> Response:
#         pass

#     @swagger_auto_schema(
#         tags=["유저"],
#         operation_summary="유저 정보 탈퇴",
#         responses={
#             status.HTTP_200_OK: BaseResponseSerializer(data_serializer=OutputSerializer),
#         },
#     )
#     def delete(self, request: Request) -> Response:
#         pass
