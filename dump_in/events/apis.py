from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from dump_in.common.base.serializers import BaseResponseSerializer, BaseSerializer
from dump_in.common.exception.exceptions import NotFoundException
from dump_in.common.pagination import LimitOffsetPagination, get_paginated_data
from dump_in.common.response import create_response
from dump_in.common.utils import inline_serializer
from dump_in.events.enums import EventHashtag
from dump_in.events.selectors.events import EventSelector
from dump_in.events.services import EventService


class EventListAPI(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (AllowAny,)

    class Pagination(LimitOffsetPagination):
        default_limit = 10

    class FilterSerializer(BaseSerializer):
        hashtag = serializers.ChoiceField(required=False, choices=[hashtag.value for hashtag in EventHashtag])
        limit = serializers.IntegerField(required=False, min_value=1, max_value=50, default=10)
        offset = serializers.IntegerField(required=False, min_value=0)

    class OutputSerializer(BaseSerializer):
        id = serializers.IntegerField()
        title = serializers.CharField()
        main_thumbnail_image_url = serializers.URLField()
        start_date = serializers.DateField()
        end_date = serializers.DateField()
        is_liked = serializers.BooleanField(default=None)
        photo_booth_brand_name = serializers.CharField(source="photo_booth_brand.name")

    @swagger_auto_schema(
        tags=["이벤트"],
        operation_summary="이벤트 목록 조회",
        query_serializer=FilterSerializer,
        responses={
            status.HTTP_200_OK: BaseResponseSerializer(data_serializer=OutputSerializer),
        },
    )
    def get(self, request: Request) -> Response:
        """
        사용자가 이벤트 목록을 조회합니다.
        url: /app/api/events
        """
        filter_serializer = self.FilterSerializer(data=request.query_params)
        filter_serializer.is_valid(raise_exception=True)
        event_selector = EventSelector()
        events = event_selector.get_event_list(
            user_id=request.user.id,
            filters=filter_serializer.validated_data,
        )
        pagination_events_data = get_paginated_data(
            pagination_class=self.Pagination,
            serializer_class=self.OutputSerializer,
            queryset=events,
            request=request,
            view=self,
        )
        return create_response(data=pagination_events_data, status_code=status.HTTP_200_OK)


class EventHomeAPI(APIView):
    authentication_classes = ()
    permission_classes = (AllowAny,)

    class Pagination(LimitOffsetPagination):
        default_limit = 10

    class InputSerializer(BaseSerializer):
        limit = serializers.IntegerField(required=False, min_value=1, max_value=50, default=10)
        offset = serializers.IntegerField(required=False, min_value=0)

    class OutputSerializer(BaseSerializer):
        id = serializers.IntegerField()
        title = serializers.CharField()
        main_thumbnail_image_url = serializers.URLField()

    @swagger_auto_schema(
        tags=["이벤트"],
        operation_summary="이벤트 홈 목록 조회",
        query_serializer=InputSerializer,
        responses={
            status.HTTP_200_OK: BaseResponseSerializer(data_serializer=OutputSerializer),
        },
    )
    def get(self, request: Request) -> Response:
        """
        사용자가 홈에서 이벤트 목록을 조회합니다.
        url: /app/api/events/home
        """
        filter_serializer = self.InputSerializer(data=request.query_params)
        filter_serializer.is_valid(raise_exception=True)
        event_selector = EventSelector()
        events = event_selector.get_event_queryset_order_by_created_at_desc()
        pagination_events_data = get_paginated_data(
            pagination_class=self.Pagination,
            serializer_class=self.OutputSerializer,
            queryset=events,
            request=request,
            view=self,
        )
        return create_response(data=pagination_events_data, status_code=status.HTTP_200_OK)


class EventDetailAPI(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (AllowAny,)

    class OutputSerializer(BaseSerializer):
        id = serializers.IntegerField()
        title = serializers.CharField()
        content = serializers.CharField()
        main_thumbnail_image_url = serializers.URLField()
        start_date = serializers.DateField()
        end_date = serializers.DateField()
        is_liked = serializers.BooleanField(default=None)
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
                "image_url": serializers.URLField(source="event_image_url"),
            },
            source="event_image",
        )

    @swagger_auto_schema(
        tags=["이벤트"],
        operation_summary="이벤트 상세 조회",
        responses={
            status.HTTP_200_OK: BaseResponseSerializer(data_serializer=OutputSerializer),
        },
    )
    def get(self, request: Request, event_id: int) -> Response:
        """
        사용자가 이벤트 상세를 조회합니다.
        url: /app/api/events/<int:event_id>
        """
        event_selector = EventSelector()
        event = event_selector.get_event_with_user_info_by_id(event_id=event_id, user_id=request.user.id)

        if event is None:
            raise NotFoundException("Event does not exist.")

        event_data = self.OutputSerializer(event).data
        return create_response(data=event_data, status_code=status.HTTP_200_OK)


class EventLikeAPI(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    class OutputSerializer(BaseSerializer):
        id = serializers.IntegerField()
        is_liked = serializers.BooleanField()

    @swagger_auto_schema(
        tags=["이벤트"],
        operation_summary="이벤트 좋아요",
        responses={
            status.HTTP_200_OK: BaseResponseSerializer(data_serializer=OutputSerializer),
        },
    )
    def post(self, request: Request, event_id: int) -> Response:
        """
        인증된 사용자가 이벤트를 좋아요 또는 좋아요 취소합니다.
        url: /app/api/events/<int:event_id>/like
        """
        event_service = EventService()
        event, is_liked = event_service.like_event(event_id=event_id, user=request.user)
        event_data = self.OutputSerializer({"id": event.id, "is_liked": is_liked}).data
        return create_response(data=event_data, status_code=status.HTTP_200_OK)
