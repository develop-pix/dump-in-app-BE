import pytest
from django.contrib.gis.geos import Point

from dump_in.photo_booths.selectors.photo_booths import PhotoBoothSelector

pytestmark = pytest.mark.django_db


class TestGetNearbyPhotoBoothQuerysetByBrandName:
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

    def test_get_nearby_photo_booth_queryset_by_brand_name_success(self, photo_booth):
        nearby_photo_booth_queryset = self.photo_booth_selector.get_nearby_photo_booth_queryset_by_brand_name(
            center_point=self.seoul_station_nearby_point,
            radius=1.5,
            photo_booth_brand_name=photo_booth.photo_booth_brand.name,
        )

        assert nearby_photo_booth_queryset.count() == 1

    def test_get_nearby_photo_booth_queryset_by_brand_name_success_distance_500m(self, photo_booth):
        nearby_photo_booth_queryset = self.photo_booth_selector.get_nearby_photo_booth_queryset_by_brand_name(
            center_point=self.seoul_millennium_hotel_point,
            radius=1.5,
            photo_booth_brand_name=photo_booth.photo_booth_brand.name,
        )

        assert nearby_photo_booth_queryset.count() == 1

    def test_get_nearby_photo_booth_queryset_by_brand_name_success_distance_1km(self, photo_booth):
        nearby_photo_booth_queryset = self.photo_booth_selector.get_nearby_photo_booth_queryset_by_brand_name(
            center_point=self.seoul_chungjeongno_station_point,
            radius=1.5,
            photo_booth_brand_name=photo_booth.photo_booth_brand.name,
        )

        assert nearby_photo_booth_queryset.count() == 1

    def test_get_nearby_photo_booth_queryset_by_brand_name_success_distance_1_5km(self, photo_booth):
        nearby_photo_booth_queryset = self.photo_booth_selector.get_nearby_photo_booth_queryset_by_brand_name(
            center_point=self.seoul_namyang_station_point,
            radius=1.5,
            photo_booth_brand_name=photo_booth.photo_booth_brand.name,
        )

        assert nearby_photo_booth_queryset.count() == 1

    def test_get_nearby_photo_booth_queryset_by_brand_name_fail_out_of_range(self, photo_booth):
        nearby_photo_booth_queryset = self.photo_booth_selector.get_nearby_photo_booth_queryset_by_brand_name(
            center_point=self.seoul_seodaemun_gu_point,
            radius=1.5,
            photo_booth_brand_name=photo_booth.photo_booth_brand.name,
        )

        assert nearby_photo_booth_queryset.count() == 0

    def test_get_nearby_photo_booth_queryset_by_brand_name_fail_photo_booth_brand_name_does_not_exist(self, photo_booth):
        nearby_photo_booth_queryset = self.photo_booth_selector.get_nearby_photo_booth_queryset_by_brand_name(
            center_point=self.seoul_station_nearby_point,
            radius=1.5,
            photo_booth_brand_name="fake_brand_name",
        )

        assert nearby_photo_booth_queryset.count() == 0
