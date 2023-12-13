from django.urls import reverse

from tests.utils import IsAuthenticateTestCase


class TestReviewListCountAPI(IsAuthenticateTestCase):
    url = reverse("api-reviews:review-list-count")

    def test_review_list_count_get_success(self, valid_review_list, valid_user):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.get(self.url)

        assert response.status_code == 200
        assert response.data["data"].get("count") == 10

    def test_review_list_count_get_success_with_filter(self, valid_review_list_frame_color, valid_user):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.get(
            self.url,
            data={"frame_color": "red"},
        )

        assert response.status_code == 200
        assert response.data["data"].get("count") == 3

    def test_review_list_count_get_fail_not_authenticated(self):
        response = self.client.get(self.url)

        assert response.status_code == 401
        assert response.data["message"] == "Authentication credentials were not provided."
