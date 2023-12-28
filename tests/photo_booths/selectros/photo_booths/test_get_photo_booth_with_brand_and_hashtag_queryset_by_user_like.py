import time

import pytest

from dump_in.photo_booths.models import PhotoBooth
from dump_in.photo_booths.selectors.photo_booths import PhotoBoothSelector

pytestmark = pytest.mark.django_db


class TestGetPhotoBoothWithBrandAndHashtagQuerysetByUserLike:
    def setup_method(self):
        self.photo_booth_selector = PhotoBoothSelector()

    def test_get_photo_booth_with_brand_and_hashtag_queryset_by_user_like_success_single_photo_booth(self, photo_booth, valid_user):
        photo_booth.user_photo_booth_like_logs.add(valid_user)

        photo_booths = self.photo_booth_selector.get_photo_booth_with_brand_and_hashtag_queryset_by_user_like(valid_user.id)

        assert str(photo_booths.first().id) == photo_booth.id

    def test_get_photo_booth_with_brand_and_hashtag_queryset_by_user_like_success_multiple_photo_booth(self, photo_booth_list, valid_user):
        for photo_booth in photo_booth_list:
            photo_booth.user_photo_booth_like_logs.add(valid_user)

        photo_booths = self.photo_booth_selector.get_photo_booth_with_brand_and_hashtag_queryset_by_user_like(valid_user.id)

        assert photo_booths.count() == len(photo_booth_list)

    def test_get_photo_booth_with_brand_and_hashtag_queryset_by_user_like_fail_does_not_exist(self, photo_booth, valid_user):
        photo_booths = self.photo_booth_selector.get_photo_booth_with_brand_and_hashtag_queryset_by_user_like(valid_user.id)

        assert photo_booths.count() == 0

    def test_get_photo_booth_with_brand_and_hashtag_queryset_by_user_like_selected_related_performance(self, photo_booth_list, valid_user):
        for photo_booth in photo_booth_list:
            photo_booth.user_photo_booth_like_logs.add(valid_user)

        start_time = time.time()

        photo_booths = PhotoBooth.objects.filter(userphotoboothlikelog__user_id=valid_user.id)

        for photo_booth in photo_booths:
            photo_booth.photo_booth_brand.name
            photo_booth.photo_booth_brand.description

        end_time = time.time()

        time_with_filter = end_time - start_time

        start_time = time.time()

        photo_booths = self.photo_booth_selector.get_photo_booth_with_brand_and_hashtag_queryset_by_user_like(valid_user.id)

        for photo_booth in photo_booths:
            photo_booth.photo_booth_brand.name
            photo_booth.photo_booth_brand.description

        end_time = time.time()

        time_with_select_related = end_time - start_time

        assert time_with_filter > time_with_select_related

    def test_get_photo_booth_with_brand_and_hashtag_queryset_by_user_like_prefetch_related_performance(self, photo_booth_list, valid_user):
        for photo_booth in photo_booth_list:
            photo_booth.user_photo_booth_like_logs.add(valid_user)

        start_time = time.time()

        photo_booths = PhotoBooth.objects.filter(userphotoboothlikelog__user_id=valid_user.id)

        for photo_booth in photo_booths:
            photo_booth.photo_booth_brand.hashtag.all()

        end_time = time.time()

        time_with_filter = end_time - start_time

        start_time = time.time()

        photo_booths = self.photo_booth_selector.get_photo_booth_with_brand_and_hashtag_queryset_by_user_like(valid_user.id)

        for photo_booth in photo_booths:
            photo_booth.photo_booth_brand.hashtag.all()

        end_time = time.time()

        time_with_prefetch_related = end_time - start_time

        assert time_with_filter > time_with_prefetch_related

    def test_get_photo_booth_with_brand_and_hashtag_queryset_by_user_like_selected_and_prefetch_related_performance(
        self, photo_booth_list, valid_user
    ):
        for photo_booth in photo_booth_list:
            photo_booth.user_photo_booth_like_logs.add(valid_user)

        start_time = time.time()

        photo_booths = PhotoBooth.objects.filter(userphotoboothlikelog__user_id=valid_user.id)

        for photo_booth in photo_booths:
            photo_booth.photo_booth_brand.name
            photo_booth.photo_booth_brand.description
            photo_booth.photo_booth_brand.hashtag.all()

        end_time = time.time()

        time_with_filter = end_time - start_time

        start_time = time.time()

        photo_booths = self.photo_booth_selector.get_photo_booth_with_brand_and_hashtag_queryset_by_user_like(valid_user.id)

        for photo_booth in photo_booths:
            photo_booth.photo_booth_brand.name
            photo_booth.photo_booth_brand.description
            photo_booth.photo_booth_brand.hashtag.all()

        end_time = time.time()

        time_with_select_and_prefetch_related = end_time - start_time

        assert time_with_filter > time_with_select_and_prefetch_related
