from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers, status
from rest_framework.exceptions import NotAuthenticated
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
from dump_in.common.pagination import LimitOffsetPagination, get_paginated_data
from dump_in.common.response import create_response
from dump_in.events.selectors.events import EventSelector
from dump_in.photo_booths.selectors.photo_booths import PhotoBoothSelector
from dump_in.photo_booths.serializers import HashtagSerializer
from dump_in.reviews.selectors.reviews import ReviewSelector
from dump_in.users.selectors.users import UserSelector
from dump_in.users.services import UserService


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
            status.HTTP_401_UNAUTHORIZED: BaseResponseExceptionSerializer(exception=NotAuthenticated),
        },
    )
    def get(self, request: Request) -> Response:
        """
        인증된 유저가 자신의 정보를 조회합니다.
        url: /app/api/auth/users/detail
        """
        user_selector = UserSelector()
        user = user_selector.get_user_by_id(user_id=request.user.id)
        user_data = self.OutputSerializer(user).data
        return create_response(data=user_data, status_code=status.HTTP_200_OK)

    @swagger_auto_schema(
        tags=["유저"],
        operation_summary="유저 정보 수정",
        responses={
            status.HTTP_200_OK: BaseResponseSerializer(data_serializer=OutputSerializer),
            status.HTTP_400_BAD_REQUEST: BaseResponseExceptionSerializer(exception=ValidationException),
            status.HTTP_401_UNAUTHORIZED: BaseResponseExceptionSerializer(exception=NotAuthenticated),
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
        user = user_service.update_user(request.user.id, input_serializer.validated_data["nickname"])
        user_data = self.OutputSerializer(user).data
        return create_response(data=user_data, status_code=status.HTTP_200_OK)

    @swagger_auto_schema(
        tags=["유저"],
        operation_summary="유저 정보 탈퇴",
        responses={
            status.HTTP_204_NO_CONTENT: "",
            status.HTTP_401_UNAUTHORIZED: BaseResponseExceptionSerializer(exception=NotAuthenticated),
        },
    )
    def delete(self, request: Request) -> Response:
        """
        인증된 유저가 자신의 정보를 탈퇴합니다. (소프트 삭제)
        url: /app/api/auth/users/detail
        """
        user_service = UserService()
        user_service.soft_delete_user(user_id=request.user.id)
        return create_response(status_code=status.HTTP_204_NO_CONTENT)


class MyReviewAPI(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    class Pagination(LimitOffsetPagination):
        default_limit = 10

    class FilterSerializer(BaseSerializer):
        limit = serializers.IntegerField(required=False)
        offset = serializers.IntegerField(required=False)

    class OutputSerializer(BaseSerializer):
        review_id = serializers.IntegerField(source="id")
        review_main_thumbnail_image_url = serializers.URLField(source="main_thumbnail_image_url")
        photo_booth_name = serializers.CharField(source="photo_booth.name")
        photo_booth_brand_name = serializers.CharField(source="photo_booth.photo_booth_brand.name")

    @swagger_auto_schema(
        tags=["유저"],
        operation_summary="내가 작성한 리뷰 조회",
        query_serializer=FilterSerializer,
        responses={
            status.HTTP_200_OK: BaseResponseSerializer(data_serializer=OutputSerializer),
            status.HTTP_401_UNAUTHORIZED: BaseResponseExceptionSerializer(exception=NotAuthenticated),
        },
    )
    def get(self, request: Request) -> Response:
        """
        인증된 유저가 자신이 작성한 리뷰를 조회합니다.
        url: /app/api/users/reviews
        """
        review_selector = ReviewSelector()
        reviews = review_selector.get_review_queryset_with_photo_booth_and_brand_by_user_id(user=request.user)
        pagination_reviews_data = get_paginated_data(
            pagination_class=self.Pagination,
            serializer_class=self.OutputSerializer,
            queryset=reviews,
            request=request,
            view=self,
        )
        return create_response(data=pagination_reviews_data, status_code=status.HTTP_200_OK)


class MyReviewLikeAPI(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    class Pagination(LimitOffsetPagination):
        default_limit = 10

    class FilterSerializer(BaseSerializer):
        limit = serializers.IntegerField(required=False)
        offset = serializers.IntegerField(required=False)

    class OutputSerializer(BaseSerializer):
        review_id = serializers.IntegerField(source="id")
        review_main_thumbnail_image_url = serializers.URLField(source="main_thumbnail_image_url")
        photo_booth_name = serializers.CharField(source="photo_booth.name")
        is_liked = serializers.BooleanField(default=True)

    @swagger_auto_schema(
        tags=["유저"],
        operation_summary="내가 좋아요한 리뷰 조회",
        query_serializer=FilterSerializer,
        responses={
            status.HTTP_200_OK: BaseResponseSerializer(data_serializer=OutputSerializer),
            status.HTTP_401_UNAUTHORIZED: BaseResponseExceptionSerializer(exception=NotAuthenticated),
        },
    )
    def get(self, request: Request) -> Response:
        """
        인증된 유저가 자신이 좋아요한 리뷰를 조회합니다.
        url: /app/api/users/reviews/likes
        """
        review_selector = ReviewSelector()
        reviews = review_selector.get_review_queryset_with_photo_booth_by_user_like(user=request.user)
        pagination_reviews_data = get_paginated_data(
            pagination_class=self.Pagination,
            serializer_class=self.OutputSerializer,
            queryset=reviews,
            request=request,
            view=self,
        )
        return create_response(data=pagination_reviews_data, status_code=status.HTTP_200_OK)


class MyPhotoBoothLikeAPI(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    class Pagination(LimitOffsetPagination):
        default_limit = 10

    class FilterSerializer(BaseSerializer):
        limit = serializers.IntegerField(required=False)
        offset = serializers.IntegerField(required=False)

    class OutputSerializer(BaseSerializer):
        photo_booth_id = serializers.UUIDField(source="id")
        photo_booth_name = serializers.CharField(source="name")
        photo_booth_brand_name = serializers.CharField(source="photo_booth_brand.name")
        photo_booth_brand_logo_image_url = serializers.URLField(source="photo_booth_brand.logo_image_url")
        hashtag = HashtagSerializer(many=True, source="photo_booth_brand.hashtag")
        is_liked = serializers.BooleanField(default=True)

    @swagger_auto_schema(
        tags=["유저"],
        operation_summary="내가 좋아요한 포토부스 조회",
        query_serializer=FilterSerializer,
        responses={
            status.HTTP_200_OK: BaseResponseSerializer(data_serializer=OutputSerializer),
            status.HTTP_401_UNAUTHORIZED: BaseResponseExceptionSerializer(exception=NotAuthenticated),
        },
    )
    def get(self, request: Request) -> Response:
        """
        인증된 유저가 자신이 좋아요한 포토부스를 조회합니다.
        url: /app/api/users/photo-booths/likes
        """
        photo_booth_selector = PhotoBoothSelector()
        photo_booths = photo_booth_selector.get_photo_booth_queryset_with_brand_and_hashtag_by_user_like(user=request.user)
        pagination_photo_booths_data = get_paginated_data(
            pagination_class=self.Pagination,
            serializer_class=self.OutputSerializer,
            queryset=photo_booths,
            request=request,
            view=self,
        )
        return create_response(data=pagination_photo_booths_data, status_code=status.HTTP_200_OK)


class MyEventLikeAPI(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    class Pagination(LimitOffsetPagination):
        default_limit = 10

    class FilterSerializer(BaseSerializer):
        limit = serializers.IntegerField(required=False)
        offset = serializers.IntegerField(required=False)

    class OutputSerializer(BaseSerializer):
        event_id = serializers.UUIDField(source="id")
        event_title = serializers.CharField(source="title")
        event_main_thumbnail_image_url = serializers.URLField(source="main_thumbnail_image_url")
        event_start_date = serializers.DateField(source="start_date")
        event_end_date = serializers.DateField(source="end_date")
        is_liked = serializers.BooleanField(default=True)

    @swagger_auto_schema(
        tags=["유저"],
        operation_summary="내가 좋아요한 이벤트 조회",
        query_serializer=FilterSerializer,
        responses={
            status.HTTP_200_OK: BaseResponseSerializer(data_serializer=OutputSerializer),
            status.HTTP_401_UNAUTHORIZED: BaseResponseExceptionSerializer(exception=NotAuthenticated),
        },
    )
    def get(self, request: Request) -> Response:
        """
        인증된 유저가 자신이 좋아요한 이벤트를 조회합니다.
        url: /app/api/users/events/likes
        """
        event_selector = EventSelector()
        events = event_selector.get_event_queryset_by_user_like(user=request.user)
        pagination_events_data = get_paginated_data(
            pagination_class=self.Pagination,
            serializer_class=self.OutputSerializer,
            queryset=events,
            request=request,
            view=self,
        )
        return create_response(data=pagination_events_data, status_code=status.HTTP_200_OK)
