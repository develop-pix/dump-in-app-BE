from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers, status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.parsers import MultiPartParser
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
from dump_in.images.services import ImageUploadService


class ImageUploadAPI(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    parser_classes = [MultiPartParser]

    class InputSerializer(BaseSerializer):
        resource_type = serializers.CharField(required=True)
        resource_type_id = serializers.IntegerField(required=True)

    class OutputSerializer(BaseSerializer):
        image_url = serializers.CharField()

    @swagger_auto_schema(
        tags=["이미지"],
        operation_summary="이미지 업로드",
        manual_parameters=[
            openapi.Parameter("image", openapi.IN_FORM, type=openapi.TYPE_FILE, required=True),
        ],
        request_body=InputSerializer,
        responses={
            status.HTTP_200_OK: BaseResponseSerializer(data_serializer=OutputSerializer),
            status.HTTP_400_BAD_REQUEST: BaseResponseExceptionSerializer(exception=ValidationException),
            status.HTTP_401_UNAUTHORIZED: BaseResponseExceptionSerializer(exception=AuthenticationFailed),
        },
    )
    def post(self, request: Request) -> Response:
        """
        인증된 사용자의 이미지를 S3에 업로드합니다. (10MB 제한)
        url: /app/api/images/upload
        """
        input_serializer = self.InputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        image_service = ImageUploadService(image_obj=request.FILES["image"], **input_serializer.validated_data)
        image_url = image_service.upload_image()
        image_data = self.OutputSerializer({"image_url": image_url}).data
        return create_response(data=image_data, status_code=status.HTTP_200_OK)
