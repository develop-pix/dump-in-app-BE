from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed

from dump_in.common.base.serializers import (
    BaseModelSerializer,
    BaseResponseExceptionSerializer,
    BaseResponseSerializer,
    BaseSerializer,
)
from dump_in.common.exception.exceptions import (
    NotFoundException,
    PermissionDeniedException,
    ValidationException,
)
from dump_in.common.pagination import LimitOffsetPagination, get_paginated_data
from dump_in.common.response import create_response
from dump_in.reviews.models import Review
from dump_in.reviews.selectors.reviews import ReviewSelector
from dump_in.reviews.services.reviews import ReviewService


class ReviewListAPI(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    class Pagination(LimitOffsetPagination):
        default_limit = 10

    class FilterSerializer(BaseSerializer):
        photo_booth_name = serializers.CharField(required=False)
        frame_color = serializers.CharField(required=False)
        participants = serializers.CharField(required=False)
        camera_shot = serializers.CharField(required=False)
        concepts = serializers.CharField(required=False)
        limit = serializers.IntegerField(required=False)
        offset = serializers.IntegerField(required=False)

    class OutputSerializer(BaseSerializer):
        review_id = serializers.IntegerField(source="id")
        review_images = serializers.StringRelatedField(many=True)  # type: ignore
        # photo_booth_name = serializers.CharField(source="photo_booth.name")

    @swagger_auto_schema(
        tags=["리뷰"],
        operation_summary="리뷰 목록 조회",
        query_serializer=FilterSerializer,
        responses={
            status.HTTP_200_OK: BaseResponseSerializer(data_serializer=OutputSerializer),
            status.HTTP_401_UNAUTHORIZED: BaseResponseExceptionSerializer(exception=AuthenticationFailed),
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
        image_urls = serializers.ListField(required=True, min_length=1, max_length=5)
        content = serializers.CharField(required=True)
        photo_booth_id = serializers.CharField(required=True)
        date = serializers.DateField(required=True)
        frame_color = serializers.CharField(required=True)
        participants = serializers.IntegerField(required=True)
        camera_shot = serializers.CharField(required=True)
        concept_ids = serializers.ListField(required=True, child=serializers.IntegerField())
        goods_amount = serializers.BooleanField(required=True, allow_null=True)
        curl_amount = serializers.BooleanField(required=False, allow_null=True)
        is_public = serializers.BooleanField(required=True)

    @swagger_auto_schema(
        tags=["리뷰"],
        operation_summary="리뷰 생성",
        request_body=InputSerializer,
        responses={
            status.HTTP_201_CREATED: BaseResponseSerializer(data_serializer=OutputSerializer),
            status.HTTP_400_BAD_REQUEST: BaseResponseExceptionSerializer(exception=ValidationException),
            status.HTTP_401_UNAUTHORIZED: BaseResponseExceptionSerializer(exception=AuthenticationFailed),
            status.HTTP_404_NOT_FOUND: BaseResponseExceptionSerializer(exception=NotFoundException),
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
        review = review_service.create_review(**input_serializer.validated_data, user=request.user)
        review_data = self.OutputSerializer(review).data
        return create_response(data=review_data, status_code=status.HTTP_201_CREATED)


class ReviewListCountAPI(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    class FilterSerializer(BaseSerializer):
        photo_booth_name = serializers.CharField(required=False)
        frame_color = serializers.CharField(required=False)
        participants = serializers.CharField(required=False)
        camera_shot = serializers.CharField(required=False)
        concepts = serializers.CharField(required=False)

    class OutputSerializer(BaseSerializer):
        count = serializers.IntegerField()

    @swagger_auto_schema(
        tags=["리뷰"],
        operation_summary="리뷰 개수 조회",
        query_serializer=FilterSerializer,
        responses={
            status.HTTP_200_OK: BaseResponseSerializer(data_serializer=OutputSerializer),
            status.HTTP_401_UNAUTHORIZED: BaseResponseExceptionSerializer(exception=AuthenticationFailed),
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

    class InputSerializer(BaseSerializer):
        image_urls = serializers.ListField(required=True, min_length=1, max_length=5)
        content = serializers.CharField(required=True)
        photo_booth_id = serializers.CharField(required=True)
        date = serializers.DateField(required=True)
        frame_color = serializers.CharField(required=True)
        participants = serializers.IntegerField(required=True)
        camera_shot = serializers.CharField(required=True)
        concept_ids = serializers.ListField(required=True, child=serializers.IntegerField())
        goods_amount = serializers.BooleanField(required=True, allow_null=True)
        curl_amount = serializers.BooleanField(required=False, allow_null=True)
        is_public = serializers.BooleanField(required=True)

    class OutputSerializer(BaseModelSerializer):
        review_images = serializers.StringRelatedField(many=True)  # type: ignore
        concepts = serializers.StringRelatedField(many=True)  # type: ignore
        is_mine = serializers.SerializerMethodField(method_name="get_is_mine")
        user = serializers.CharField(source="user.nickname")

        class Meta:
            model = Review
            exclude = ["is_deleted", "is_public", "user_review_like_logs"]

        def get_is_mine(self, obj):
            if self.context["user"] == obj.user:
                return True
            return False

    @swagger_auto_schema(
        tags=["리뷰"],
        operation_summary="리뷰 상세 조회",
        responses={
            status.HTTP_200_OK: BaseResponseSerializer(data_serializer=OutputSerializer),
            status.HTTP_401_UNAUTHORIZED: BaseResponseExceptionSerializer(exception=AuthenticationFailed),
            status.HTTP_403_FORBIDDEN: BaseResponseExceptionSerializer(exception=PermissionDeniedException),
            status.HTTP_404_NOT_FOUND: BaseResponseExceptionSerializer(exception=NotFoundException),
        },
    )
    def get(self, request: Request, review_id: int) -> Response:
        """
        인증된 사용자가 포토부스에 대한 리뷰를 조회합니다.
        url: /app/api/reviews/<int:review_id>
        """
        review_service = ReviewService()
        review = review_service.view_count_up(review_id=review_id, user=request.user)
        review_data = self.OutputSerializer(review, context={"user": request.user}).data
        return create_response(data=review_data, status_code=status.HTTP_200_OK)

    @swagger_auto_schema(
        tags=["리뷰"],
        operation_summary="리뷰 수정",
        request_body=InputSerializer,
        responses={
            status.HTTP_200_OK: BaseResponseSerializer(data_serializer=OutputSerializer),
            status.HTTP_400_BAD_REQUEST: BaseResponseExceptionSerializer(exception=ValidationException),
            status.HTTP_401_UNAUTHORIZED: BaseResponseExceptionSerializer(exception=AuthenticationFailed),
            status.HTTP_403_FORBIDDEN: BaseResponseExceptionSerializer(exception=PermissionDeniedException),
            status.HTTP_404_NOT_FOUND: BaseResponseExceptionSerializer(exception=NotFoundException),
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
        review = review_service.update_review(review_id=review_id, **input_serializer.validated_data, user=request.user)
        review_data = self.OutputSerializer(review, context={"user": request.user}).data
        return create_response(data=review_data, status_code=status.HTTP_200_OK)

    @swagger_auto_schema(
        tags=["리뷰"],
        operation_summary="리뷰 삭제",
        responses={
            status.HTTP_204_NO_CONTENT: "",
            status.HTTP_401_UNAUTHORIZED: BaseResponseExceptionSerializer(exception=AuthenticationFailed),
            status.HTTP_403_FORBIDDEN: BaseResponseExceptionSerializer(exception=PermissionDeniedException),
            status.HTTP_404_NOT_FOUND: BaseResponseExceptionSerializer(exception=NotFoundException),
        },
    )
    def delete(self, request: Request, review_id: int) -> Response:
        """
        인증된 사용자가 포토부스에 대한 자신의 리뷰를 삭제합니다.
        url: /app/api/reviews/<int:review_id>
        """
        review_service = ReviewService()
        review_service.soft_delete_review(review_id=review_id, user=request.user)
        return create_response(status_code=status.HTTP_204_NO_CONTENT)


class ReviewLikeAPI(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    class OutputSerializer(BaseSerializer):
        review_id = serializers.IntegerField()
        is_liked = serializers.BooleanField()

    @swagger_auto_schema(
        tags=["리뷰"],
        operation_summary="리뷰 좋아요",
        responses={
            status.HTTP_200_OK: BaseResponseSerializer(data_serializer=OutputSerializer),
            status.HTTP_401_UNAUTHORIZED: BaseResponseExceptionSerializer(exception=AuthenticationFailed),
            status.HTTP_404_NOT_FOUND: BaseResponseExceptionSerializer(exception=NotFoundException),
        },
    )
    def post(self, request: Request, review_id: int) -> Response:
        """
        인증된 사용자가 포토부스에 대한 리뷰를 좋아요 또는 좋아요 취소합니다.
        url: /app/api/reviews/<int:review_id>/likes
        """
        review_service = ReviewService()
        review, is_liked = review_service.like_review(review_id=review_id, user=request.user)
        review_data = self.OutputSerializer(data={"review_id": review.id, "is_liked": is_liked}).data
        return create_response(data=review_data, status_code=status.HTTP_200_OK)
