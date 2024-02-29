import uuid

import pytest

from dump_in.photo_booths.selectors.photo_booths import PhotoBoothSelector

pytestmark = pytest.mark.django_db


class TestGetPhotoBoothQuerySetByName:
    def setup_method(self):
        self.photo_booth_selector = PhotoBoothSelector()

    def test_get_photo_booth_queryset_by_name_success(self, photo_booth):
        photo_booth_queryset = self.photo_booth_selector.get_photo_booth_queryset_by_name(photo_booth.name)

        assert str(photo_booth_queryset.first().id) == photo_booth.id

    def test_get_photo_booth_queryset_by_name_fail_does_not_exist(self):
        photo_booth_queryset = self.photo_booth_selector.get_photo_booth_queryset_by_name(str(uuid.uuid4()))

        assert photo_booth_queryset.count() == 0
