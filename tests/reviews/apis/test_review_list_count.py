from django.urls import reverse

from tests.utils import IsAuthenticateTestCase


class TestReviewListCountAPI(IsAuthenticateTestCase):
    url = reverse("api-reviews:review-list-count")

    def test_review_list_count_get_success(self, review_list, new_users):
        access_token = self.obtain_token(new_users)
        self.authenticate_with_token(access_token)
        response = self.client.get(self.url)

        assert response.status_code == 200
        assert response.data["data"] == {
            "count": 7,
        }

    def test_review_list_count_get_success_with_filter(self, review_list, new_users):
        access_token = self.obtain_token(new_users)
        self.authenticate_with_token(access_token)
        response = self.client.get(
            self.url,
            data={"frame_color": "red"},
        )

        assert response.status_code == 200
        assert response.data["data"] == {
            "count": 3,
        }

    def test_review_list_count_get_fail_not_authenticated(self):
        response = self.client.get(self.url)

        assert response.status_code == 401
        assert response.data["message"] == "자격 인증데이터(authentication credentials)가 제공되지 않았습니다."
