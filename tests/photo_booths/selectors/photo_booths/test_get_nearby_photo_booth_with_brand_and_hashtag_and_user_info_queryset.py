import pytest
from django.contrib.gis.geos import Point

from dump_in.photo_booths.selectors.photo_booths import PhotoBoothSelector

pytestmark = pytest.mark.django_db


class TestGetNearbyPhotoBoothtWithBrandAndHashtagAndUserInfoQueryset:
    def setup_method(self):
        self.photo_booth_selector = PhotoBoothSelector()
        self.seoul_station_nearby_point = Point(
            x=126.97151987127677,
            y=37.55558726825372,
            srid=4326,
        )
        self.seoul_seodaemun_gu_point = Point(
            x=126.9491255577525,
            y=37.58900890890801,
            srid=4326,
        )
        self.seoul_millennium_hotel_point = Point(
            x=126.97559998078428,
            y=37.55496649353846,
            srid=4326,
        )  # 서울역과 500m
        self.seoul_chungjeongno_station_point = Point(
            x=126.96456344507027,
            y=37.55962185314878,
            srid=4326,
        )  # 서울역과 1km
        self.seoul_namyang_station_point = Point(
            x=126.97129314924726,
            y=37.54181094401603,
            srid=4326,
        )  # 서울역과 1.5km

    def test_get_nearby_photo_booth_with_brand_and_hashtag_and_user_info_queryset_success_single_photo_booth(self, photo_booth, valid_user):
        nearby_photo_booth_queryset = self.photo_booth_selector.get_nearby_photo_booth_with_brand_and_hashtag_and_user_info_queryset(
            center_point=self.seoul_station_nearby_point,
            radius=1.5,
            user=valid_user,
        )

        assert str(nearby_photo_booth_queryset.first().id) == photo_booth.id

    def test_get_nearby_photo_booth_with_brand_and_hashtag_and_user_info_queryset_success_multiple_photo_booth(
        self, photo_booth_list, valid_user
    ):
        nearby_photo_booth_queryset = self.photo_booth_selector.get_nearby_photo_booth_with_brand_and_hashtag_and_user_info_queryset(
            center_point=self.seoul_station_nearby_point,
            radius=1.5,
            user=valid_user,
        )

        assert nearby_photo_booth_queryset.count() == len(photo_booth_list)

    def test_get_nearby_photo_booth_with_brand_and_hashtag_and_user_info_queryset_success_distance_500m(self, photo_booth, valid_user):
        nearby_photo_booth_queryset = self.photo_booth_selector.get_nearby_photo_booth_with_brand_and_hashtag_and_user_info_queryset(
            center_point=self.seoul_millennium_hotel_point,
            radius=1.5,
            user=valid_user,
        )

        assert str(nearby_photo_booth_queryset.first().id) == photo_booth.id

    def test_get_nearby_photo_booth_with_brand_and_hashtag_and_user_info_queryset_success_distance_1km(self, photo_booth, valid_user):
        nearby_photo_booth_queryset = self.photo_booth_selector.get_nearby_photo_booth_with_brand_and_hashtag_and_user_info_queryset(
            center_point=self.seoul_chungjeongno_station_point,
            radius=1.5,
            user=valid_user,
        )

        assert str(nearby_photo_booth_queryset.first().id) == photo_booth.id

    def test_get_nearby_photo_booth_with_brand_and_hashtag_and_user_info_queryset_success_distance_1_5km(self, photo_booth, valid_user):
        nearby_photo_booth_queryset = self.photo_booth_selector.get_nearby_photo_booth_with_brand_and_hashtag_and_user_info_queryset(
            center_point=self.seoul_namyang_station_point,
            radius=1.5,
            user=valid_user,
        )

        assert str(nearby_photo_booth_queryset.first().id) == photo_booth.id

    def test_get_nearby_photo_booth_with_brand_and_hashtag_and_user_info_queryset_success_is_liked_true(self, photo_booth, valid_user):
        photo_booth.user_photo_booth_like_logs.add(valid_user)

        nearby_photo_booth_queryset = self.photo_booth_selector.get_nearby_photo_booth_with_brand_and_hashtag_and_user_info_queryset(
            center_point=self.seoul_station_nearby_point,
            radius=1.5,
            user=valid_user,
        )

        assert nearby_photo_booth_queryset.first().is_liked is True

    def test_get_nearby_photo_booth_with_brand_and_hashtag_and_user_info_queryset_success_is_liked_false(self, photo_booth, valid_user):
        nearby_photo_booth_queryset = self.photo_booth_selector.get_nearby_photo_booth_with_brand_and_hashtag_and_user_info_queryset(
            center_point=self.seoul_station_nearby_point,
            radius=1.5,
            user=valid_user,
        )

        assert nearby_photo_booth_queryset.first().is_liked is False

    def test_get_nearby_photo_booth_with_brand_and_hashtag_and_user_info_queryset_success_anonymous_user(self, photo_booth, inactive_user):
        nearby_photo_booth_queryset = self.photo_booth_selector.get_nearby_photo_booth_with_brand_and_hashtag_and_user_info_queryset(
            center_point=self.seoul_station_nearby_point,
            radius=1.5,
            user=inactive_user,
        )

        assert str(nearby_photo_booth_queryset.first().id) == photo_booth.id

    def test_get_nearby_photo_booth_with_brand_and_hashtag_and_user_info_queryset_fail_out_of_range(self, photo_booth, valid_user):
        nearby_photo_booth_queryset = self.photo_booth_selector.get_nearby_photo_booth_with_brand_and_hashtag_and_user_info_queryset(
            center_point=self.seoul_seodaemun_gu_point,
            radius=1.5,
            user=valid_user,
        )

        assert nearby_photo_booth_queryset.count() == 0
