from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed

from dump_in.common.base.serializers import (
    BaseResponseExceptionSerializer,
    BaseResponseSerializer,
    BaseSerializer,
)
from dump_in.common.response import create_response
from dump_in.photo_booths.selectors.photo_booth_brands import PhotoBoothBrandSelector


class PhotoBoothBrandListAPI(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    class OutputSerializer(BaseSerializer):
        id = serializers.IntegerField()
        name = serializers.CharField()
        logo_image_url = serializers.URLField()

    @swagger_auto_schema(
        tags=["포토부스"],
        operation_summary="포토부스 업체 조회",
        responses={
            status.HTTP_200_OK: BaseResponseSerializer(data_serializer=OutputSerializer),
            status.HTTP_401_UNAUTHORIZED: BaseResponseExceptionSerializer(exception=AuthenticationFailed),
        },
    )
    def get(self, request: Request) -> Response:
        """
        인증된 사용자가 포토부스에 업체를 조회합니다.
        url: /app/api/photo-booths/brands
        """
        photo_booth_brand_selector = PhotoBoothBrandSelector()
        photo_booth_brands = photo_booth_brand_selector.get_photo_booth_queryset()
        photo_booth_brands_data = self.OutputSerializer(photo_booth_brands, many=True).data
        return create_response(data=photo_booth_brands_data, status_code=status.HTTP_200_OK)
