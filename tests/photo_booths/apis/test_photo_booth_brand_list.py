from django.urls import reverse

from tests.utils import IsAuthenticateTestCase


class TestPhotoBoothBrandListAPI(IsAuthenticateTestCase):
    url = reverse("api-photo-booths:photo-booth-brand-list")

    def test_photo_booth_brand_list_get_success(self, photo_booth_brand, new_users):
        access_token = self.obtain_token(new_users)
        self.authenticate_with_token(access_token)
        response = self.client.get(self.url)

        assert response.status_code == 200
        assert response.data["data"] is not None

    def test_photo_booth_brand_list_get_fail_not_authenticated(self):
        response = self.client.get(self.url)

        assert response.status_code == 401
        assert response.data["message"] == "자격 인증데이터(authentication credentials)가 제공되지 않았습니다."
