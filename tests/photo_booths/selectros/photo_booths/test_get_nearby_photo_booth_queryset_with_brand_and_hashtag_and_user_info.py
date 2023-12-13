import time

import pytest
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import Distance
from django.db.models import BooleanField, Case, When

from dump_in.photo_booths.models import PhotoBooth
from dump_in.photo_booths.selectors.photo_booths import PhotoBoothSelector

pytestmark = pytest.mark.django_db


class TestGetNearbyPhotoBoothQuerySetWithBrandAndHashtagAndUserInfo:
    def setup_method(self):
        self.photo_booth_selector = PhotoBoothSelector()
        self.seoul_station_nearby_point = Point(
            x=37.55558726825372,
            y=126.97151987127677,
            srid=4326,
        )
        self.seoul_seodaemun_gu_point = Point(
            x=37.58900890890801,
            y=126.9491255577525,
            srid=4326,
        )
        self.seoul_millennium_hotel_point = Point(
            x=37.55496649353846,
            y=126.97559998078428,
            srid=4326,
        )  # 서울역과 500m
        self.seoul_chungjeongno_station_point = Point(
            x=37.55962185314878,
            y=126.96456344507027,
            srid=4326,
        )  # 서울역과 1km
        self.seoul_namyang_station_point = Point(
            x=37.54004499549353,
            y=126.97133908632812,
            srid=4326,
        )  # 서울역과 1.5km

    def test_get_nearby_photo_booth_queryset_with_brand_and_hashtag_and_user_info_success(self, photo_booth, valid_user):
        nearby_photo_booth_queryset = self.photo_booth_selector.get_nearby_photo_booth_queryset_with_brand_and_hashtag_and_user_info(
            center_point=self.seoul_station_nearby_point,
            radius=1.5,
            user=valid_user,
        )

        assert nearby_photo_booth_queryset.count() == 1

    def test_get_nearby_photo_booth_queryset_with_brand_and_hashtag_and_user_info_success_distance_500m(self, photo_booth, valid_user):
        nearby_photo_booth_queryset = self.photo_booth_selector.get_nearby_photo_booth_queryset_with_brand_and_hashtag_and_user_info(
            center_point=self.seoul_millennium_hotel_point,
            radius=1.5,
            user=valid_user,
        )

        assert nearby_photo_booth_queryset.count() == 1

    def test_get_nearby_photo_booth_queryset_with_brand_and_hashtag_and_user_info_success_distance_1km(self, photo_booth, valid_user):
        nearby_photo_booth_queryset = self.photo_booth_selector.get_nearby_photo_booth_queryset_with_brand_and_hashtag_and_user_info(
            center_point=self.seoul_chungjeongno_station_point,
            radius=1.5,
            user=valid_user,
        )

        assert nearby_photo_booth_queryset.count() == 1

    def test_get_nearby_photo_booth_queryset_with_brand_and_hashtag_and_user_info_success_distance_1_5km(self, photo_booth, valid_user):
        nearby_photo_booth_queryset = self.photo_booth_selector.get_nearby_photo_booth_queryset_with_brand_and_hashtag_and_user_info(
            center_point=self.seoul_namyang_station_point,
            radius=1.5,
            user=valid_user,
        )

        assert nearby_photo_booth_queryset.count() == 1

    def test_get_nearby_photo_booth_queryset_with_brand_and_hashtag_and_user_info_success_is_liked_true(self, photo_booth, valid_user):
        photo_booth.user_photo_booth_like_logs.add(valid_user)

        nearby_photo_booth_queryset = self.photo_booth_selector.get_nearby_photo_booth_queryset_with_brand_and_hashtag_and_user_info(
            center_point=self.seoul_station_nearby_point,
            radius=1.5,
            user=valid_user,
        )

        assert nearby_photo_booth_queryset.first().is_liked == True

    def test_get_nearby_photo_booth_queryset_with_brand_and_hashtag_and_user_info_success_is_liked_false(self, photo_booth, valid_user):
        nearby_photo_booth_queryset = self.photo_booth_selector.get_nearby_photo_booth_queryset_with_brand_and_hashtag_and_user_info(
            center_point=self.seoul_station_nearby_point,
            radius=1.5,
            user=valid_user,
        )

        assert nearby_photo_booth_queryset.first().is_liked == False

    def test_get_nearby_photo_booth_queryset_with_brand_and_hashtag_and_user_info_fail_out_of_range(self, photo_booth, valid_user):
        nearby_photo_booth_queryset = self.photo_booth_selector.get_nearby_photo_booth_queryset_with_brand_and_hashtag_and_user_info(
            center_point=self.seoul_seodaemun_gu_point,
            radius=1.5,
            user=valid_user,
        )

        assert nearby_photo_booth_queryset.count() == 0

    def test_get_nearby_photo_booth_queryset_with_brand_and_hashtag_and_user_info_select_related_performance(
        self, photo_booth_list, valid_user
    ):
        start_time = time.time()

        nearby_photo_booth_queryset = PhotoBooth.objects.annotate(
            is_liked=Case(
                When(userphotoboothlikelog__user=valid_user, then=True),
                default=False,
                output_field=BooleanField(),
            ),
        ).filter(
            point__distance_lte=(self.seoul_station_nearby_point, Distance(km=1.5)),
        )

        for photo_booth in nearby_photo_booth_queryset:
            photo_booth.photo_booth_brand.name
            photo_booth.photo_booth_brand.description

        end_time = time.time()

        time_with_filter = end_time - start_time

        start_time = time.time()

        nearby_photo_booth_queryset = self.photo_booth_selector.get_nearby_photo_booth_queryset_with_brand_and_hashtag_and_user_info(
            center_point=self.seoul_station_nearby_point,
            radius=1.5,
            user=valid_user,
        )

        for photo_booth in nearby_photo_booth_queryset:
            photo_booth.photo_booth_brand.name
            photo_booth.photo_booth_brand.description

        end_time = time.time()

        time_with_select_related = end_time - start_time

        assert time_with_filter > time_with_select_related

    def test_get_nearby_photo_booth_queryset_with_brand_and_hashtag_and_user_info_prefetch_related_performance(
        self, photo_booth_list, valid_user
    ):
        start_time = time.time()

        nearby_photo_booth_queryset = PhotoBooth.objects.annotate(
            is_liked=Case(
                When(userphotoboothlikelog__user=valid_user, then=True),
                default=False,
                output_field=BooleanField(),
            ),
        ).filter(
            point__distance_lte=(self.seoul_station_nearby_point, Distance(km=1.5)),
        )

        for photo_booth in nearby_photo_booth_queryset:
            photo_booth.photo_booth_brand.hashtag.all()

        end_time = time.time()

        time_with_filter = end_time - start_time

        start_time = time.time()

        nearby_photo_booth_queryset = self.photo_booth_selector.get_nearby_photo_booth_queryset_with_brand_and_hashtag_and_user_info(
            center_point=self.seoul_station_nearby_point,
            radius=1.5,
            user=valid_user,
        )

        for photo_booth in nearby_photo_booth_queryset:
            photo_booth.photo_booth_brand.hashtag.all()

        end_time = time.time()

        time_with_prefetch_related = end_time - start_time

        assert time_with_filter > time_with_prefetch_related

    def test_get_nearby_photo_booth_queryset_with_brand_and_hashtag_and_user_info_prefetch_and_selected_related_performance(
        self, photo_booth_list, valid_user
    ):
        start_time = time.time()

        nearby_photo_booth_queryset = PhotoBooth.objects.annotate(
            is_liked=Case(
                When(userphotoboothlikelog__user=valid_user, then=True),
                default=False,
                output_field=BooleanField(),
            ),
        ).filter(
            point__distance_lte=(self.seoul_station_nearby_point, Distance(km=1.5)),
        )

        for photo_booth in nearby_photo_booth_queryset:
            photo_booth.photo_booth_brand.hashtag.all()
            photo_booth.photo_booth_brand.name
            photo_booth.photo_booth_brand.description

        end_time = time.time()

        time_with_filter = end_time - start_time

        start_time = time.time()

        nearby_photo_booth_queryset = self.photo_booth_selector.get_nearby_photo_booth_queryset_with_brand_and_hashtag_and_user_info(
            center_point=self.seoul_station_nearby_point,
            radius=1.5,
            user=valid_user,
        )

        for photo_booth in nearby_photo_booth_queryset:
            photo_booth.photo_booth_brand.hashtag.all()
            photo_booth.photo_booth_brand.name
            photo_booth.photo_booth_brand.description

        end_time = time.time()

        time_with_prefetch_related = end_time - start_time

        assert time_with_filter > time_with_prefetch_related
