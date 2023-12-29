from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from dump_in.common.base.serializers import BaseResponseSerializer, BaseSerializer
from dump_in.common.pagination import LimitOffsetPagination, get_paginated_data
from dump_in.common.response import create_response
from dump_in.common.utils import inline_serializer
from dump_in.events.selectors.events import EventSelector
from dump_in.photo_booths.selectors.photo_booths import PhotoBoothSelector
from dump_in.reviews.selectors.reviews import ReviewSelector
from dump_in.users.selectors.notifications import NotificationSelector
from dump_in.users.selectors.users import UserSelector
from dump_in.users.services.notifications import NotificationService
from dump_in.users.services.user_mobile_tokens import UserMobileTokenService
from dump_in.users.services.users import UserService


class UserDetailAPI(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    class InputSerializer(BaseSerializer):
        nickname = serializers.CharField(required=True, max_length=16)

    class OutputSerializer(BaseSerializer):
        id = serializers.IntegerField()
        email = serializers.EmailField()
        nickname = serializers.CharField()

    @swagger_auto_schema(
        tags=["유저"],
        operation_summary="유저 정보 조회",
        responses={
            status.HTTP_200_OK: BaseResponseSerializer(data_serializer=OutputSerializer),
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
        },
        request_body=InputSerializer,
    )
    def put(self, request: Request) -> Response:
        """
        인증된 유저가 자신의 정보를 수정합니다. (닉네임)
        url: /app/api/auth/users/detail
        """
        input_serializer = self.InputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        user_service = UserService()
        user = user_service.update_user(user_id=request.user.id, nickname=input_serializer.validated_data["nickname"])
        user_data = self.OutputSerializer(user).data
        return create_response(data=user_data, status_code=status.HTTP_200_OK)

    @swagger_auto_schema(
        tags=["유저"],
        operation_summary="유저 정보 탈퇴",
        responses={
            status.HTTP_204_NO_CONTENT: "",
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
        limit = serializers.IntegerField(required=False, min_value=1, max_value=50, default=10)
        offset = serializers.IntegerField(required=False, min_value=0)

    class OutputSerializer(BaseSerializer):
        id = serializers.IntegerField()
        photo_booth_name = serializers.CharField(source="photo_booth.name")
        photo_booth_brand_name = serializers.CharField(source="photo_booth.photo_booth_brand.name")
        main_thumbnail_image_url = serializers.URLField()

    @swagger_auto_schema(
        tags=["유저"],
        operation_summary="내가 작성한 리뷰 목록 조회",
        query_serializer=FilterSerializer,
        responses={
            status.HTTP_200_OK: BaseResponseSerializer(data_serializer=OutputSerializer),
        },
    )
    def get(self, request: Request) -> Response:
        """
        인증된 유저가 자신이 작성한 리뷰 목록을 조회합니다.
        url: /app/api/users/reviews
        """
        filter_serializer = self.FilterSerializer(data=request.query_params)
        filter_serializer.is_valid(raise_exception=True)
        review_selector = ReviewSelector()
        reviews = review_selector.get_review_with_photo_booth_and_brand_queryset_by_user_id(user_id=request.user.id)
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
        limit = serializers.IntegerField(required=False, min_value=1, max_value=50, default=10)
        offset = serializers.IntegerField(required=False, min_value=0)

    class OutputSerializer(BaseSerializer):
        id = serializers.IntegerField()
        photo_booth_name = serializers.CharField(source="photo_booth.name")
        main_thumbnail_image_url = serializers.URLField()
        is_liked = serializers.BooleanField(default=True)

    @swagger_auto_schema(
        tags=["유저"],
        operation_summary="내가 좋아요한 리뷰 목록 조회",
        query_serializer=FilterSerializer,
        responses={
            status.HTTP_200_OK: BaseResponseSerializer(data_serializer=OutputSerializer),
        },
    )
    def get(self, request: Request) -> Response:
        """
        인증된 유저가 자신이 좋아요한 리뷰 목록을 조회합니다.
        url: /app/api/users/reviews/likes
        """
        filter_serializer = self.FilterSerializer(data=request.query_params)
        filter_serializer.is_valid(raise_exception=True)
        review_selector = ReviewSelector()
        reviews = review_selector.get_review_with_photo_booth_queryset_by_user_like(user_id=request.user.id)
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
        limit = serializers.IntegerField(required=False, min_value=1, max_value=50, default=10)
        offset = serializers.IntegerField(required=False, min_value=0)

    class OutputSerializer(BaseSerializer):
        id = serializers.UUIDField()
        photo_booth_name = serializers.CharField(source="name")
        photo_booth_brand_name = serializers.CharField(source="photo_booth_brand.name")
        photo_booth_brand_logo_image_url = serializers.URLField(source="photo_booth_brand.logo_image_url")
        hashtag = inline_serializer(
            many=True,
            fields={
                "id": serializers.IntegerField(),
                "name": serializers.CharField(),
            },
            source="photo_booth_brand.hashtag",
        )
        is_liked = serializers.BooleanField(default=True)

    @swagger_auto_schema(
        tags=["유저"],
        operation_summary="내가 좋아요한 포토부스 목록 조회",
        query_serializer=FilterSerializer,
        responses={
            status.HTTP_200_OK: BaseResponseSerializer(data_serializer=OutputSerializer),
        },
    )
    def get(self, request: Request) -> Response:
        """
        인증된 유저가 자신이 좋아요한 포토부스 목록을 조회합니다.
        url: /app/api/users/photo-booths/likes
        """
        filter_serializer = self.FilterSerializer(data=request.query_params)
        filter_serializer.is_valid(raise_exception=True)
        photo_booth_selector = PhotoBoothSelector()
        photo_booths = photo_booth_selector.get_photo_booth_with_brand_and_hashtag_queryset_by_user_like(user_id=request.user.id)
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
        limit = serializers.IntegerField(required=False, min_value=1, max_value=50, default=10)
        offset = serializers.IntegerField(required=False, min_value=0)

    class OutputSerializer(BaseSerializer):
        id = serializers.IntegerField()
        title = serializers.CharField()
        main_thumbnail_image_url = serializers.URLField()
        start_date = serializers.DateField()
        end_date = serializers.DateField()
        is_liked = serializers.BooleanField(default=True)

    @swagger_auto_schema(
        tags=["유저"],
        operation_summary="내가 좋아요한 이벤트 목록 조회",
        query_serializer=FilterSerializer,
        responses={
            status.HTTP_200_OK: BaseResponseSerializer(data_serializer=OutputSerializer),
        },
    )
    def get(self, request: Request) -> Response:
        """
        인증된 유저가 자신이 좋아요한 이벤트 목록을 조회합니다.
        url: /app/api/users/events/likes
        """
        filter_serializer = self.FilterSerializer(data=request.query_params)
        filter_serializer.is_valid(raise_exception=True)
        event_selector = EventSelector()
        events = event_selector.get_event_queryset_by_user_like(user_id=request.user.id)
        pagination_events_data = get_paginated_data(
            pagination_class=self.Pagination,
            serializer_class=self.OutputSerializer,
            queryset=events,
            request=request,
            view=self,
        )
        return create_response(data=pagination_events_data, status_code=status.HTTP_200_OK)


class NotificationListAPI(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    class OutputSerializer(BaseSerializer):
        id = serializers.IntegerField()
        title = serializers.CharField()
        content = serializers.CharField()
        is_read = serializers.BooleanField()
        parameter_data = serializers.CharField()
        created_at = serializers.DateTimeField()
        updated_at = serializers.DateTimeField()
        category = serializers.CharField(source="category.name")

    @swagger_auto_schema(
        tags=["유저"],
        operation_summary="알림 목록 조회",
        responses={
            status.HTTP_200_OK: BaseResponseSerializer(data_serializer=OutputSerializer),
        },
    )
    def get(self, request: Request) -> Response:
        """
        인증된 유저가 자신의 알림 목록을 조회합니다.
        url: /app/api/users/notifications
        """
        notification_selector = NotificationSelector()
        notifications = notification_selector.get_notification_with_category_queryset_by_user_id(user_id=request.user.id)
        notifications_data = self.OutputSerializer(notifications, many=True).data
        return create_response(data=notifications_data, status_code=status.HTTP_200_OK)

    @swagger_auto_schema(
        tags=["유저"],
        operation_summary="알림 전체 삭제",
        responses={
            status.HTTP_204_NO_CONTENT: "",
        },
    )
    def delete(self, request: Request) -> Response:
        """
        인증된 유저가 자신의 알림을 삭제합니다.
        url: /app/api/users/notifications
        """
        notification_service = NotificationService()
        notification_service.soft_delete_notifications(user_id=request.user.id)
        return create_response(status_code=status.HTTP_204_NO_CONTENT)


class NotificationCheckAPI(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    class OutputSerializer(BaseSerializer):
        is_unread = serializers.BooleanField()
        count = serializers.IntegerField()

    @swagger_auto_schema(
        tags=["유저"],
        operation_summary="알림 확인",
        responses={
            status.HTTP_200_OK: BaseResponseSerializer(data_serializer=OutputSerializer),
        },
    )
    def get(self, request: Request) -> Response:
        """
        인증된 유저가 자신의 알림을 확인합니다.
        url: /app/api/users/notifications/check
        """
        notification_selector = NotificationSelector()
        is_unread = notification_selector.check_unread_notification_by_user_id(user_id=request.user.id)
        notification_count = notification_selector.get_unread_notification_count_by_user_id(user_id=request.user.id)
        notification_data = self.OutputSerializer(
            {
                "is_unread": is_unread,
                "count": notification_count,
            }
        ).data
        return create_response(data=notification_data, status_code=status.HTTP_200_OK)


class NotificationDetailAPI(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    class OutputSerializer(BaseSerializer):
        id = serializers.IntegerField()
        title = serializers.CharField()
        content = serializers.CharField()
        is_read = serializers.BooleanField()
        parameter_data = serializers.CharField()
        created_at = serializers.DateTimeField()
        updated_at = serializers.DateTimeField()
        category = serializers.CharField(source="category.name")

    @swagger_auto_schema(
        tags=["유저"],
        operation_summary="알림 읽음 처리",
        responses={
            status.HTTP_200_OK: BaseResponseSerializer(data_serializer=OutputSerializer),
        },
    )
    def put(self, request: Request, notification_id: int) -> Response:
        """
        인증된 유저가 자신의 알림을 읽음 처리합니다.
        url: /app/api/users/notifications/<int:notification_id>
        """
        notification_service = NotificationService()
        notification = notification_service.read_notification(notification_id=notification_id, user_id=request.user.id)
        notification_data = self.OutputSerializer(notification).data
        return create_response(data=notification_data, status_code=status.HTTP_200_OK)


class UserMobileTokenAPI(APIView):
    authentication_classes = ()
    permission_classes = (AllowAny,)

    class InputSerializer(BaseSerializer):
        mobile_token = serializers.CharField(required=True, max_length=512)

    class OutputSerializer(BaseSerializer):
        id = serializers.IntegerField()
        mobile_token = serializers.CharField(source="token")

    @swagger_auto_schema(
        tags=["유저"],
        operation_summary="모바일 토큰 등록",
        request_body=InputSerializer,
        responses={
            status.HTTP_201_CREATED: BaseResponseSerializer(data_serializer=OutputSerializer),
        },
    )
    def post(self, request: Request) -> Response:
        """
        인증되지 않은 유저가 모바일 토큰을 등록합니다.
        url: /app/api/users/mobile-token
        """
        input_serializer = self.InputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        user_mobile_token_service = UserMobileTokenService()
        user_mobile_token = user_mobile_token_service.create_user_mobile_token(token=input_serializer.validated_data["mobile_token"])
        user_mobile_token_data = self.OutputSerializer(user_mobile_token).data
        return create_response(data=user_mobile_token_data, status_code=status.HTTP_201_CREATED)
