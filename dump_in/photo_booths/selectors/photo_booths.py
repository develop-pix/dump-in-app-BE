from typing import Optional, Union

from django.contrib.auth.models import AnonymousUser
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import Distance
from django.db.models import BooleanField, Case, QuerySet, When

from dump_in.photo_booths.models import PhotoBooth
from dump_in.users.models import User


class PhotoBoothSelector:
    def get_photo_booth_by_id(self, photo_booth_id: str) -> Optional[PhotoBooth]:
        try:
            return PhotoBooth.objects.filter(id=photo_booth_id).get()
        except PhotoBooth.DoesNotExist:
            return None

    def get_photo_booth_queryset_by_name(self, name: str) -> QuerySet[PhotoBooth]:
        return PhotoBooth.objects.filter(name__icontains=name)

    def get_photo_booth_with_user_info_by_id(self, photo_booth_id: str, user: Union[User, AnonymousUser]) -> Optional[PhotoBooth]:
        try:
            qs = PhotoBooth.objects.filter(id=photo_booth_id)

            if user.is_authenticated:
                like_id_list = user.userphotoboothlikelog_set.values_list("photo_booth_id", flat=True)

                qs = qs.annotate(
                    is_liked=Case(
                        When(id__in=like_id_list, then=True),
                        default=False,
                        output_field=BooleanField(),
                    ),
                )
            return qs.get()
        except PhotoBooth.DoesNotExist:
            return None

    def get_nearby_photo_booth_with_brand_and_hashtag_and_user_info_queryset(
        self, center_point: Point, radius: int, user: Union[User, AnonymousUser]
    ) -> QuerySet[PhotoBooth]:
        qs = (
            PhotoBooth.objects.select_related("photo_booth_brand")
            .prefetch_related("photo_booth_brand__hashtag")
            .filter(point__distance_lte=(center_point, Distance(km=radius)))
        )
        if user.is_authenticated:
            like_id_list = user.userphotoboothlikelog_set.values_list("photo_booth_id", flat=True)

            qs = qs.annotate(
                is_liked=Case(
                    When(id__in=like_id_list, then=True),
                    default=False,
                    output_field=BooleanField(),
                ),
            )
        return qs

    def get_nearby_photo_booth_queryset_by_brand_name(
        self, center_point: Point, radius: int, photo_booth_brand_name: str
    ) -> QuerySet[PhotoBooth]:
        return PhotoBooth.objects.filter(
            point__distance_lte=(center_point, Distance(km=radius)),
            photo_booth_brand__name__icontains=photo_booth_brand_name,
        )

    def get_photo_booth_with_brand_and_hashtag_queryset_by_user_like(self, user_id) -> QuerySet[PhotoBooth]:
        return (
            PhotoBooth.objects.select_related("photo_booth_brand")
            .prefetch_related("photo_booth_brand__hashtag")
            .filter(userphotoboothlikelog__user_id=user_id)
        )
