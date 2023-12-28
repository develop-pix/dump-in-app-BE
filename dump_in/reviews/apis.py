from django.core.validators import MaxValueValidator
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from dump_in.common.base.serializers import BaseResponseSerializer, BaseSerializer
from dump_in.common.fields import CustomMultipleChoiceField
from dump_in.common.pagination import LimitOffsetPagination, get_paginated_data
from dump_in.common.response import create_response
from dump_in.common.utils import inline_serializer
from dump_in.photo_booths.enums import PhotoBoothLocation
from dump_in.reviews.enums import CameraShot, Concept, FrameColor, Participants
from dump_in.reviews.selectors.reviews import ReviewSelector
from dump_in.reviews.services import ReviewService


class ReviewListAPI(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    class Pagination(LimitOffsetPagination):
        default_limit = 10

    class FilterSerializer(BaseSerializer):
        photo_booth_location = CustomMultipleChoiceField(
            required=False, choices=[photo_booth_location.value for photo_booth_location in PhotoBoothLocation]
        )
        frame_color = CustomMultipleChoiceField(required=False, choices=[frame_color.value for frame_color in FrameColor])
        participants = CustomMultipleChoiceField(required=False, choices=[participants.value for participants in Participants])
        camera_shot = CustomMultipleChoiceField(required=False, choices=[camera_shot.value for camera_shot in CameraShot])
        concept = CustomMultipleChoiceField(required=False, choices=[concept.value for concept in Concept])
        limit = serializers.IntegerField(required=False, min_value=1, max_value=50, default=10)
        offset = serializers.IntegerField(required=False, min_value=0)

    class OutputSerializer(BaseSerializer):
        id = serializers.IntegerField()
        main_thumbnail_image_url = serializers.URLField()
        photo_booth_name = serializers.CharField(source="photo_booth.name")

    @swagger_auto_schema(
        tags=["리뷰"],
        operation_summary="리뷰 목록 조회",
        query_serializer=FilterSerializer,
        responses={
            status.HTTP_200_OK: BaseResponseSerializer(data_serializer=OutputSerializer),
        },
    )
    def get(self, request: Request) -> Response:
        """
        인증된 사용자가 포토부스에 대한 리뷰 목록을 조회합니다.
        url: /app/api/reviews/
        """
        filter_serializer = self.FilterSerializer(data=request.query_params)
        filter_serializer.is_valid(raise_exception=True)
        review_selector = ReviewSelector()
        reviews = review_selector.get_review_list(filters=filter_serializer.validated_data)
        pagination_reviews_data = get_paginated_data(
            pagination_class=self.Pagination,
            serializer_class=self.OutputSerializer,
            queryset=reviews,
            request=request,
            view=self,
        )
        return create_response(data=pagination_reviews_data, status_code=status.HTTP_200_OK)

    class InputSerializer(BaseSerializer):
        main_thumbnail_image_url = serializers.URLField(required=True)
        image_urls = serializers.ListField(max_length=4, child=serializers.URLField())
        content = serializers.CharField(required=True, max_length=100)
        photo_booth_id = serializers.UUIDField(required=True)
        date = serializers.DateField(required=True, validators=[MaxValueValidator(limit_value=timezone.now().date())])
        frame_color = serializers.ChoiceField(required=True, choices=[frame_color.value for frame_color in FrameColor])
        participants = serializers.IntegerField(required=True, min_value=1, max_value=5)
        camera_shot = serializers.ChoiceField(required=True, choices=[camera_shot.value for camera_shot in CameraShot])
        concept_names = CustomMultipleChoiceField(choices=[concept.value for concept in Concept], max_choices=5, allow_empty=False)
        goods_amount = serializers.BooleanField(required=False, allow_null=True)
        curl_amount = serializers.BooleanField(required=False, allow_null=True)
        is_public = serializers.BooleanField(required=True)

    @swagger_auto_schema(
        tags=["리뷰"],
        operation_summary="리뷰 생성",
        request_body=InputSerializer,
        responses={
            status.HTTP_201_CREATED: BaseResponseSerializer(data_serializer=OutputSerializer),
        },
    )
    def post(self, request: Request) -> Response:
        """
        인증된 사용자가 포토부스에 대한 리뷰를 생성합니다.
        url: /app/api/reviews/
        """
        input_serializer = self.InputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        review_service = ReviewService()
        review = review_service.create_review(**input_serializer.validated_data, user_id=request.user.id)
        review_data = self.OutputSerializer(review).data
        return create_response(data=review_data, status_code=status.HTTP_201_CREATED)


class ReviewListCountAPI(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    class FilterSerializer(BaseSerializer):
        photo_booth_location = CustomMultipleChoiceField(
            required=False, choices=[photo_booth_location.value for photo_booth_location in PhotoBoothLocation]
        )
        frame_color = CustomMultipleChoiceField(required=False, choices=[frame_color.value for frame_color in FrameColor])
        participants = CustomMultipleChoiceField(required=False, choices=[participants.value for participants in Participants])
        camera_shot = CustomMultipleChoiceField(required=False, choices=[camera_shot.value for camera_shot in CameraShot])
        concept = CustomMultipleChoiceField(required=False, choices=[concept.value for concept in Concept])

    class OutputSerializer(BaseSerializer):
        count = serializers.IntegerField()

    @swagger_auto_schema(
        tags=["리뷰"],
        operation_summary="리뷰 개수 조회",
        query_serializer=FilterSerializer,
        responses={
            status.HTTP_200_OK: BaseResponseSerializer(data_serializer=OutputSerializer),
        },
    )
    def get(self, request: Request) -> Response:
        """
        인증된 사용자가 포토부스에 대한 리뷰 개수를 조회합니다.
        url: /app/api/reviews/count
        """
        filter_serializer = self.FilterSerializer(data=request.query_params)
        filter_serializer.is_valid(raise_exception=True)
        review_selector = ReviewSelector()
        reviews_count = review_selector.get_review_count(filters=filter_serializer.validated_data)
        reviews_data = self.OutputSerializer(data={"count": reviews_count}).data
        return create_response(data=reviews_data, status_code=status.HTTP_200_OK)


class ReviewDetailAPI(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    class GetOutputSerializer(BaseSerializer):
        id = serializers.IntegerField()
        image = inline_serializer(
            many=True,
            fields={
                "id": serializers.IntegerField(),
                "image_url": serializers.URLField(source="review_image_url"),
            },
            source="review_image",
        )
        concept = inline_serializer(
            many=True,
            fields={
                "id": serializers.IntegerField(),
                "name": serializers.CharField(),
            },
        )
        is_mine = serializers.BooleanField()
        is_liked = serializers.BooleanField()
        user_nickname = serializers.CharField(source="user.nickname")
        created_at = serializers.DateTimeField()
        updated_at = serializers.DateTimeField()
        content = serializers.CharField()
        main_thumbnail_image_url = serializers.URLField()
        date = serializers.DateField()
        frame_color = serializers.CharField()
        participants = serializers.IntegerField()
        camera_shot = serializers.CharField()
        goods_amount = serializers.BooleanField()
        curl_amount = serializers.BooleanField()
        is_public = serializers.BooleanField()
        view_count = serializers.IntegerField()
        like_count = serializers.IntegerField()
        photo_booth_id = serializers.UUIDField()

    @swagger_auto_schema(
        tags=["리뷰"],
        operation_summary="리뷰 상세 조회",
        responses={
            status.HTTP_200_OK: BaseResponseSerializer(data_serializer=GetOutputSerializer),
        },
    )
    def get(self, request: Request, review_id: int) -> Response:
        """
        인증된 사용자가 포토부스에 대한 리뷰를 조회합니다.
        url: /app/api/reviews/<int:review_id>
        """
        review_service = ReviewService()
        review = review_service.view_count_up(review_id=review_id, user_id=request.user.id)
        review_data = self.GetOutputSerializer(review).data
        return create_response(data=review_data, status_code=status.HTTP_200_OK)

    class InputSerializer(BaseSerializer):
        main_thumbnail_image_url = serializers.URLField(required=True)
        image_urls = serializers.ListField(max_length=4, child=serializers.URLField())
        content = serializers.CharField(required=True, max_length=100)
        photo_booth_id = serializers.UUIDField(required=True)
        date = serializers.DateField(required=True, validators=[MaxValueValidator(limit_value=timezone.now().date())])
        frame_color = serializers.ChoiceField(required=True, choices=[frame_color.value for frame_color in FrameColor])
        participants = serializers.IntegerField(required=True, min_value=1, max_value=5)
        camera_shot = serializers.ChoiceField(required=True, choices=[camera_shot.value for camera_shot in CameraShot])
        concept_names = CustomMultipleChoiceField(choices=[concept.value for concept in Concept], max_choices=5, allow_empty=False)
        goods_amount = serializers.BooleanField(required=False, allow_null=True)
        curl_amount = serializers.BooleanField(required=False, allow_null=True)
        is_public = serializers.BooleanField(required=True)

    class PutOutputSerializer(BaseSerializer):
        id = serializers.IntegerField()
        main_thumbnail_image_url = serializers.URLField()
        photo_booth_name = serializers.CharField(source="photo_booth.name")
        image = inline_serializer(
            many=True,
            fields={
                "id": serializers.IntegerField(),
                "image_url": serializers.URLField(source="review_image_url"),
            },
            source="review_image",
        )
        concept = inline_serializer(
            many=True,
            fields={
                "id": serializers.IntegerField(),
                "name": serializers.CharField(),
            },
        )
        user_nickname = serializers.CharField(source="user.nickname")
        created_at = serializers.DateTimeField()
        updated_at = serializers.DateTimeField()
        content = serializers.CharField()
        date = serializers.DateField()
        frame_color = serializers.CharField()
        participants = serializers.IntegerField()
        camera_shot = serializers.CharField()
        goods_amount = serializers.BooleanField()
        curl_amount = serializers.BooleanField()
        is_public = serializers.BooleanField()
        view_count = serializers.IntegerField()
        like_count = serializers.IntegerField()
        photo_booth_id = serializers.UUIDField()

    @swagger_auto_schema(
        tags=["리뷰"],
        operation_summary="리뷰 수정",
        request_body=InputSerializer,
        responses={
            status.HTTP_200_OK: BaseResponseSerializer(data_serializer=PutOutputSerializer),
        },
    )
    def put(self, request: Request, review_id: int) -> Response:
        """
        인증된 사용자가 포토부스에 대한 자신의 리뷰를 수정합니다.
        url: /app/api/reviews/<int:review_id>
        """
        input_serializer = self.InputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        review_service = ReviewService()
        review = review_service.update_review(review_id=review_id, user_id=request.user.id, **input_serializer.validated_data)
        review_data = self.PutOutputSerializer(review).data
        return create_response(data=review_data, status_code=status.HTTP_200_OK)

    @swagger_auto_schema(
        tags=["리뷰"],
        operation_summary="리뷰 삭제",
        responses={
            status.HTTP_204_NO_CONTENT: "",
        },
    )
    def delete(self, request: Request, review_id: int) -> Response:
        """
        인증된 사용자가 포토부스에 대한 자신의 리뷰를 삭제합니다.
        url: /app/api/reviews/<int:review_id>
        """
        review_service = ReviewService()
        review_service.soft_delete_review(review_id=review_id, user_id=request.user.id)
        return create_response(status_code=status.HTTP_204_NO_CONTENT)


class ReviewLikeAPI(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    class OutputSerializer(BaseSerializer):
        id = serializers.IntegerField()
        is_liked = serializers.BooleanField()

    @swagger_auto_schema(
        tags=["리뷰"],
        operation_summary="리뷰 좋아요",
        responses={
            status.HTTP_200_OK: BaseResponseSerializer(data_serializer=OutputSerializer),
        },
    )
    def post(self, request: Request, review_id: int) -> Response:
        """
        인증된 사용자가 포토부스에 대한 리뷰를 좋아요 또는 좋아요 취소합니다.
        url: /app/api/reviews/<int:review_id>/likes
        """
        review_service = ReviewService()
        review, is_liked = review_service.like_review(review_id=review_id, user=request.user)
        review_data = self.OutputSerializer(data={"id": review.id, "is_liked": is_liked}).data
        return create_response(data=review_data, status_code=status.HTTP_200_OK)
