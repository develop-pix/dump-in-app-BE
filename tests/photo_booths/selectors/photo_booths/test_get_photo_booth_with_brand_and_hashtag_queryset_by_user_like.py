import pytest

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
