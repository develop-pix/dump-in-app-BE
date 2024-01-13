import pytest
from django.urls import reverse

from tests.utils import IsAuthenticateTestCase

pytestmark = pytest.mark.django_db


class TestPhotoBoothBrandList(IsAuthenticateTestCase):
    url = reverse("api-photo-booths:photo-booth-brand-list")

    def test_photo_booth_brand_list_get_success(self, photo_booth_brand_list, valid_user):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.get(self.url)

        assert response.status_code == 200
        assert len(response.data["data"]) == 3

    def test_photo_booth_brand_list_get_success_anonymous_user(self, photo_booth_brand_list):
        response = self.client.get(self.url)

        assert response.status_code == 200
        assert len(response.data["data"]) == 3
