from typing import Optional

from django.contrib.gis.geos import Point
from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from dump_in.common.base.serializers import BaseResponseSerializer, BaseSerializer
from dump_in.common.exception.exceptions import NotFoundException
from dump_in.common.response import create_response
from dump_in.common.utils import inline_serializer
from dump_in.events.selectors.events import EventSelector
from dump_in.photo_booths.selectors.photo_booth_brand_images import (
    PhotoBoothBrandImageSelector,
)
from dump_in.photo_booths.selectors.photo_booth_brands import PhotoBoothBrandSelector
from dump_in.photo_booths.selectors.photo_booths import PhotoBoothSelector
from dump_in.photo_booths.services import PhotoBoothService
from dump_in.reviews.selectors.reviews import ReviewSelector


class PhotoBoothBrandListAPI(APIView):
    authentication_classes = ()
    permission_classes = (AllowAny,)

    class OutputSerializer(BaseSerializer):
        id = serializers.IntegerField()
        name = serializers.CharField()
        logo_image_url = serializers.URLField()

    @swagger_auto_schema(
        tags=["포토부스"],
        operation_summary="포토부스 업체 목록 조회",
        responses={
            status.HTTP_200_OK: BaseResponseSerializer(data_serializer=OutputSerializer),
        },
    )
    def get(self, request: Request) -> Response:
        """
        인증된 사용자가 포토부스에 업체 목록을 조회합니다.
        url: /app/api/photo-booths/brands
        """
        photo_booth_brand_selector = PhotoBoothBrandSelector()
        photo_booth_brands = photo_booth_brand_selector.get_photo_booth_brand_queryset()
        photo_booth_brands_data = self.OutputSerializer(photo_booth_brands, many=True).data
        return create_response(data=photo_booth_brands_data, status_code=status.HTTP_200_OK)


class PhotoBoothBrandDetailAPI(APIView):
    authentication_classes = ()
    permission_classes = (AllowAny,)

    class OutputSerializer(BaseSerializer):
        id = serializers.IntegerField()
        name = serializers.CharField()
        hashtag = inline_serializer(
            many=True,
            fields={
                "id": serializers.IntegerField(),
                "name": serializers.CharField(),
            },
        )
        image = inline_serializer(
            many=True,
            fields={
                "id": serializers.IntegerField(),
                "image_url": serializers.CharField(source="photo_booth_brand_image_url"),
            },
        )

    @swagger_auto_schema(
        tags=["포토부스"],
        operation_summary="포토부스 업체 상세 조회",
        responses={
            status.HTTP_200_OK: BaseResponseSerializer(data_serializer=OutputSerializer),
        },
    )
    def get(self, request: Request, photo_booth_brand_id: int) -> Response:
        """
        인증된 사용자가 포토부스에 업체를 상세 조회합니다.
        url: /app/api/photo-booths/brands/<int:photo_booth_brand_id>
        """
        photo_booth_brand_selector = PhotoBoothBrandSelector()
        photo_booth_brand = photo_booth_brand_selector.get_photo_booth_brand_by_id(photo_booth_brand_id=photo_booth_brand_id)

        if photo_booth_brand is None:
            raise NotFoundException("Photo Booth Brand does not exist")

        photo_booth_brand_image_selector = PhotoBoothBrandImageSelector()
        photo_booth_brand_image = photo_booth_brand_image_selector.get_recent_photo_booth_brand_image_queryset_by_photo_booth_brand_id(
            photo_booth_brand_id=photo_booth_brand_id
        )

        photo_booth_brand_data = self.OutputSerializer(
            {
                "id": photo_booth_brand.id,
                "name": photo_booth_brand.name,
                "hashtag": photo_booth_brand.hashtag,
                "image": photo_booth_brand_image,
            },
        ).data
        return create_response(data=photo_booth_brand_data, status_code=status.HTTP_200_OK)


class PhotoBoothBrandEventListAPI(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (AllowAny,)

    class FilterSerializer(BaseSerializer):
        limit = serializers.IntegerField(default=15, min_value=1, max_value=50)

    class OutputSerializer(BaseSerializer):
        id = serializers.IntegerField()
        title = serializers.CharField()
        main_thumbnail_image_url = serializers.URLField()
        start_date = serializers.DateField()
        end_date = serializers.DateField()
        is_liked = serializers.BooleanField(default=None)

    @swagger_auto_schema(
        tags=["포토부스"],
        operation_summary="포토부스 업체 이벤트 목록 조회",
        responses={
            status.HTTP_200_OK: BaseResponseSerializer(data_serializer=OutputSerializer),
        },
    )
    def get(self, request: Request, photo_booth_brand_id: int) -> Response:
        """
        인증된 사용자가 포토부스에 업체 이벤트 목록을 조회합니다.
        url: /app/api/photo-booths/brands/<int:photo_booth_brand_id>/events
        """
        filter_serializer = self.FilterSerializer(data=request.query_params)
        filter_serializer.is_valid(raise_exception=True)
        limit = filter_serializer.validated_data["limit"]

        photo_booth_brand_selector = PhotoBoothBrandSelector()
        photo_booth_brand = photo_booth_brand_selector.get_photo_booth_brand_by_id(photo_booth_brand_id=photo_booth_brand_id)

        if photo_booth_brand is None:
            raise NotFoundException("Photo Booth Brand does not exist")

        event_selector = EventSelector()
        events = event_selector.get_event_queryset_by_photo_booth_brand_id(
            photo_booth_brand_id=photo_booth_brand_id,
            user_id=request.user.id,
        ).order_by("-created_at")[0:limit]
        events_data = self.OutputSerializer(events, many=True).data
        return create_response(data=events_data, status_code=status.HTTP_200_OK)


class PhotoBoothBrandReviewListAPI(APIView):
    authentication_classes = ()
    permission_classes = (AllowAny,)

    class FilterSerializer(BaseSerializer):
        limit = serializers.IntegerField(default=15, min_value=1, max_value=50)

    class OutputSerializer(BaseSerializer):
        id = serializers.IntegerField()
        main_thumbnail_image_url = serializers.URLField()
        content = serializers.CharField()
        frame_color = serializers.CharField()
        participants = serializers.IntegerField()
        camera_shot = serializers.CharField()
        goods_amount = serializers.BooleanField()
        curl_amount = serializers.BooleanField()
        concept = inline_serializer(
            many=True,
            fields={
                "id": serializers.IntegerField(),
                "name": serializers.CharField(),
            },
        )
        created_at = serializers.DateTimeField()
        updated_at = serializers.DateTimeField()

    @swagger_auto_schema(
        tags=["포토부스"],
        operation_summary="포토부스 업체 리뷰 목록 조회",
        responses={
            status.HTTP_200_OK: BaseResponseSerializer(data_serializer=OutputSerializer),
        },
    )
    def get(self, request: Request, photo_booth_brand_id: int) -> Response:
        """
        인증된 사용자가 포토부스에 업체 리뷰 목록을 조회합니다.
        url: /app/api/photo-booths/brands/<int:photo_booth_brand_id>/reviews
        """
        filter_serializer = self.FilterSerializer(data=request.query_params)
        filter_serializer.is_valid(raise_exception=True)
        limit = filter_serializer.validated_data["limit"]

        photo_booth_brand_selector = PhotoBoothBrandSelector()
        photo_booth_brand = photo_booth_brand_selector.get_photo_booth_brand_by_id(photo_booth_brand_id=photo_booth_brand_id)

        if photo_booth_brand is None:
            raise NotFoundException("Photo Booth Brand does not exist")

        review_selector = ReviewSelector()
        reviews = review_selector.get_review_with_concept_queryset_by_photo_booth_brand_id(
            photo_booth_brand_id=photo_booth_brand_id,
        ).order_by("-created_at")[0:limit]
        reviews_data = self.OutputSerializer(reviews, many=True).data
        return create_response(data=reviews_data, status_code=status.HTTP_200_OK)


class PhotoBoothLocationSearchAPI(APIView):
    authentication_classes = ()
    permission_classes = (AllowAny,)

    class FilterSerializer(BaseSerializer):
        photo_booth_brand_name = serializers.CharField(required=True, max_length=64)
        latitude = serializers.FloatField(required=True, min_value=-90, max_value=90)
        longitude = serializers.FloatField(required=True, min_value=-180, max_value=180)
        radius = serializers.FloatField(required=True, min_value=0, max_value=1.5)

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
        operation_summary="포토부스 지점 위치 검색",
        query_serializer=FilterSerializer,
        responses={
            status.HTTP_200_OK: BaseResponseSerializer(data_serializer=OutputSerializer),
        },
    )
    def get(self, request: Request) -> Response:
        """
        인증된 사용자가 자신의 위치를 기준으로 포토부스 지점 위치를 검색합니다. (반경 최대 1.5km)
        url: /app/api/photo-booths/locations/search
        """
        filter_serializer = self.FilterSerializer(data=request.query_params)
        filter_serializer.is_valid(raise_exception=True)
        center_point = Point(
            x=filter_serializer.validated_data["longitude"],
            y=filter_serializer.validated_data["latitude"],
            srid=4326,
        )
        photo_booths_selector = PhotoBoothSelector()
        photo_booths = photo_booths_selector.get_nearby_photo_booth_queryset_by_brand_name(
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


class PhotoBoothLocationListAPI(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (AllowAny,)

    class FilterSerializer(BaseSerializer):
        latitude = serializers.FloatField(required=True, min_value=-90, max_value=90)
        longitude = serializers.FloatField(required=True, min_value=-180, max_value=180)
        radius = serializers.FloatField(required=True, min_value=0, max_value=1.5)

    class OutputSerializer(BaseSerializer):
        id = serializers.UUIDField()
        name = serializers.CharField()
        latitude = serializers.FloatField()
        longitude = serializers.FloatField()
        is_liked = serializers.BooleanField(default=None)
        photo_booth_brand = inline_serializer(
            fields={
                "name": serializers.CharField(),
                "logo_image_url": serializers.CharField(),
                "hashtag": inline_serializer(
                    many=True,
                    fields={
                        "id": serializers.IntegerField(),
                        "name": serializers.CharField(),
                    },
                ),
            }
        )
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
        operation_summary="포토부스 지점 위치 목록 조회",
        query_serializer=FilterSerializer,
        responses={
            status.HTTP_200_OK: BaseResponseSerializer(data_serializer=OutputSerializer),
        },
    )
    def get(self, request: Request) -> Response:
        """
        인증된 사용자가 자신의 위치를 기준으로 포토부스 지점 목록을 조회합니다. (반경 1.5km)
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
        photo_booths = photo_booths_selector.get_nearby_photo_booth_with_brand_and_hashtag_and_user_info_queryset(
            center_point=center_point,
            radius=filter_serializer.validated_data["radius"],
            user_id=request.user.id,
        )
        photo_booths_data = self.OutputSerializer(
            photo_booths,
            many=True,
            context={"center_point": center_point},
        ).data
        return create_response(data=photo_booths_data, status_code=status.HTTP_200_OK)


class PhotoBoothDetailAPI(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (AllowAny,)

    class FilterSerializer(BaseSerializer):
        latitude = serializers.FloatField(required=False, min_value=-90, max_value=90)
        longitude = serializers.FloatField(required=False, min_value=-180, max_value=180)

    class OutputSerializer(BaseSerializer):
        id = serializers.UUIDField()
        name = serializers.CharField()
        latitude = serializers.FloatField()
        longitude = serializers.FloatField()
        street_address = serializers.CharField()
        road_address = serializers.CharField()
        operation_time = serializers.CharField()
        is_liked = serializers.BooleanField(default=None)
        photo_booth_brand = inline_serializer(
            fields={
                "name": serializers.CharField(),
                "image": inline_serializer(
                    many=True,
                    fields={
                        "id": serializers.IntegerField(),
                        "image_url": serializers.CharField(source="photo_booth_brand_image_url"),
                    },
                ),
                "hashtag": inline_serializer(
                    many=True,
                    fields={
                        "id": serializers.IntegerField(),
                        "name": serializers.CharField(),
                    },
                ),
            }
        )
        distance = serializers.SerializerMethodField()

        def get_distance(self, obj) -> Optional[str]:
            center_point = self.context["center_point"]
            if center_point is not None:
                destination_point = obj.get("point")
                distance = center_point.distance(destination_point)
                if distance > 0.01:
                    return f"{distance * 100:.2f} km"
                return f"{distance * 100000:.2f} m"
            return None

    @swagger_auto_schema(
        tags=["포토부스"],
        operation_summary="포토부스 지점 상세 조회",
        query_serializer=FilterSerializer,
        responses={
            status.HTTP_200_OK: BaseResponseSerializer(data_serializer=OutputSerializer),
        },
    )
    def get(self, request: Request, photo_booth_id: str) -> Response:
        """
        인증된 사용자가 포토부스 지점 상세 정보를 조회합니다.
        url: /app/api/photo-booths/<str:photo_booth_id>
        """
        filter_serializer = self.FilterSerializer(data=request.query_params)
        filter_serializer.is_valid(raise_exception=True)

        longitude = filter_serializer.validated_data.get("longitude")
        latitude = filter_serializer.validated_data.get("latitude")
        center_point = None

        if longitude is not None and latitude is not None:
            center_point = Point(
                x=longitude,
                y=latitude,
                srid=4326,
            )

        photo_booth_selector = PhotoBoothSelector()
        photo_booth = photo_booth_selector.get_photo_booth_with_user_info_by_id(
            photo_booth_id=photo_booth_id,
            user_id=request.user.id,
        )

        if photo_booth is None:
            raise NotFoundException("Photo Booth does not exist")

        if photo_booth.photo_booth_brand_id is not None:
            photo_booth_brand_image_selector = PhotoBoothBrandImageSelector()
            photo_booth_brand_image = photo_booth_brand_image_selector.get_recent_photo_booth_brand_image_queryset_by_photo_booth_brand_id(
                photo_booth_brand_id=photo_booth.photo_booth_brand_id
            )

        photo_booth_data = self.OutputSerializer(
            {
                "id": photo_booth.id,
                "name": photo_booth.name,
                "latitude": photo_booth.latitude,
                "longitude": photo_booth.longitude,
                "street_address": photo_booth.street_address,
                "road_address": photo_booth.road_address,
                "operation_time": photo_booth.operation_time,
                "is_liked": getattr(photo_booth, "is_liked", None),
                "photo_booth_brand": {
                    "name": getattr(photo_booth.photo_booth_brand, "name", None),
                    "image": photo_booth_brand_image,
                    "hashtag": getattr(photo_booth.photo_booth_brand, "hashtag", []),
                },
                "point": photo_booth.point,
            },
            context={"center_point": center_point},
        ).data
        return create_response(data=photo_booth_data, status_code=status.HTTP_200_OK)


class PhotoBoothLikeAPI(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    class OutputSerializer(BaseSerializer):
        id = serializers.UUIDField()
        is_liked = serializers.BooleanField()

    @swagger_auto_schema(
        tags=["포토부스"],
        operation_summary="포토부스 지점 좋아요",
        responses={
            status.HTTP_200_OK: BaseResponseSerializer(data_serializer=OutputSerializer),
        },
    )
    def post(self, request: Request, photo_booth_id: str) -> Response:
        """
        인증된 사용자가 포토부스 지점을 좋아요 또는 좋아요 취소합니다.
        url: /app/api/photo-booths/<str:photo_booth_id>/likes
        """
        photo_booth_service = PhotoBoothService()
        photo_booth, is_liked = photo_booth_service.like_photo_booth(photo_booth_id=photo_booth_id, user=request.user)
        photo_booth_data = self.OutputSerializer({"id": photo_booth.id, "is_liked": is_liked}).data
        return create_response(data=photo_booth_data, status_code=status.HTTP_200_OK)


class PhotoBoothReviewListAPI(APIView):
    authentication_classes = ()
    permission_classes = (AllowAny,)

    class FilterSerializer(BaseSerializer):
        limit = serializers.IntegerField(default=15, min_value=1, max_value=50)

    class OutputSerializer(BaseSerializer):
        id = serializers.IntegerField()
        main_thumbnail_image_url = serializers.URLField()
        content = serializers.CharField()
        frame_color = serializers.CharField()
        participants = serializers.IntegerField()
        camera_shot = serializers.CharField()
        goods_amount = serializers.BooleanField()
        curl_amount = serializers.BooleanField()
        concept = inline_serializer(
            many=True,
            fields={
                "id": serializers.IntegerField(),
                "name": serializers.CharField(),
            },
        )
        created_at = serializers.DateTimeField()
        updated_at = serializers.DateTimeField()

    @swagger_auto_schema(
        tags=["포토부스"],
        operation_summary="포토부스 지점 리뷰 목록 조회",
        query_serializer=FilterSerializer,
        responses={
            status.HTTP_200_OK: BaseResponseSerializer(data_serializer=OutputSerializer),
        },
    )
    def get(self, request: Request, photo_booth_id: str) -> Response:
        """
        인증된 사용자가 포토부스 지점 리뷰 목록을 조회합니다.
        url: /app/api/photo-booths/<str:photo_booth_id>/reviews
        """
        filter_serializer = self.FilterSerializer(data=request.query_params)
        filter_serializer.is_valid(raise_exception=True)
        limit = filter_serializer.validated_data["limit"]
        review_selector = ReviewSelector()
        reviews = review_selector.get_review_with_concept_queryset_by_photo_booth_id(
            photo_booth_id=photo_booth_id,
        ).order_by(
            "-created_at"
        )[0:limit]
        reviews_data = self.OutputSerializer(reviews, many=True).data
        return create_response(data=reviews_data, status_code=status.HTTP_200_OK)
