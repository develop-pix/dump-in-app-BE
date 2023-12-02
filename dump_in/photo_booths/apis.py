from django.contrib.gis.geos import Point
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
from dump_in.photo_booths.selectors.photo_booths import PhotoBoothSelector


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


class PhotoBoothLocationSearchAPI(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    class FilterSerializer(BaseSerializer):
        photo_booth_brand_name = serializers.CharField(required=True)
        latitude = serializers.FloatField(required=True)
        longitude = serializers.FloatField(required=True)
        radius = serializers.ChoiceField(choices=[0.5, 1, 1.5], required=True)

    class OutputSerializer(BaseSerializer):
        id = serializers.UUIDField()
        name = serializers.CharField()
        distance = serializers.SerializerMethodField()

        def get_distance(self, obj) -> str:
            center_point = self.context["center_point"]
            destination_point = obj.point
            distance = center_point.distance(destination_point)
            if distance > 0.01:
                return f"{distance * 100:.2f} km"
            return f"{distance * 100000:.2f} m"

    @swagger_auto_schema(
        tags=["포토부스"],
        operation_summary="포토부스 위치 조회",
        query_serializer=FilterSerializer,
        responses={
            status.HTTP_200_OK: BaseResponseSerializer(data_serializer=OutputSerializer),
            status.HTTP_401_UNAUTHORIZED: BaseResponseExceptionSerializer(exception=AuthenticationFailed),
        },
    )
    def get(self, request: Request) -> Response:
        """
        인증된 사용자가 포토부스 위치를 조회합니다. (원 반지름 500m, 1km, 1.5km)
        url: /app/api/photo-booths/locations
        """
        filter_serializer = self.FilterSerializer(data=request.query_params)
        filter_serializer.is_valid(raise_exception=True)
        center_point = Point(
            x=filter_serializer.validated_data["longitude"],
            y=filter_serializer.validated_data["latitude"],
            srid=4326,
        )
        photo_booths_selector = PhotoBoothSelector()
        photo_booths = photo_booths_selector.get_nearby_photo_booth_queryset_by_photo_booth_brand_name(
            center_point=center_point,
            radius=filter_serializer.validated_data["radius"],
            photo_booth_brand_name=filter_serializer.validated_data["photo_booth_brand_name"],
        )
        photo_booths_data = self.OutputSerializer(
            photo_booths,
            many=True,
            context={"center_point": center_point},
        ).data
        return create_response(data=photo_booths_data, status_code=status.HTTP_200_OK)


# class PhotoBoothDetailAPI(APIView):
#     authentication_classes = (JWTAuthentication,)
#     permission_classes = (IsAuthenticated,)

#     class FilterSerializer(BaseSerializer):
#         latitude = serializers.FloatField()
#         longitude = serializers.FloatField()

#     @swagger_auto_schema(
#         tags=["포토부스"],
#         operation_summary="포토부스 상세 조회",
#         responses={
#             # status.HTTP_200_OK: BaseResponseSerializer(data_serializer=OutputSerializer),
#             status.HTTP_401_UNAUTHORIZED: BaseResponseExceptionSerializer(exception=AuthenticationFailed),
#         },
#     )
#     def get(self, request: Request, photo_booth_id: str) -> Response:
#         """
#         인증된 사용자가 포토부스 상세 정보를 조회합니다.
#         url: /app/api/photo-booths/<str:photo_booth_id>
#         """
#         filter_serializer = self.FilterSerializer(data=request.query_params)
#         filter_serializer.is_valid(raise_exception=True)
