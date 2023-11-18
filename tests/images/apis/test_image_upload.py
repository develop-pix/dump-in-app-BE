import tempfile

import pytest
from django.test.client import BOUNDARY, MULTIPART_CONTENT, encode_multipart
from django.urls import reverse
from PIL import Image

from tests.utils import IdAuthenticateTestCase

pytestmark = pytest.mark.django_db


class TestImageUploadAPI(IdAuthenticateTestCase):
    url = reverse("api-images:upload")

    def get_temporary_image(self, temp_file):
        size = (200, 200)
        color = (255, 0, 0, 0)
        image = Image.new("RGBA", size, color)
        image.save(temp_file, "png")
        return temp_file

    def test_image_upload_success(self, new_users, mocker):
        mocker.patch("django.core.files.storage.default_storage.save")

        temp_file = tempfile.NamedTemporaryFile()
        temp_file.name = "image.png"
        image_file = self.get_temporary_image(temp_file)
        image_file.seek(0)

        access_token = self.obtain_token(new_users)
        self.authenticate_with_token(access_token)

        response = self.client.post(
            path=self.url,
            content_type=MULTIPART_CONTENT,
            data=encode_multipart(
                data={
                    "image": image_file,
                    "resource_type": "photo_booth",
                    "resource_type_id": "1",
                },
                boundary=BOUNDARY,
            ),
        )

        assert response.status_code == 200
        assert response.data["data"]["image_url"] is not None

    def test_image_upload_fail_not_authenticated(self, mocker):
        mocker.patch("django.core.files.storage.default_storage.save")

        temp_file = tempfile.NamedTemporaryFile()
        temp_file.name = "image.png"
        image_file = self.get_temporary_image(temp_file)
        image_file.seek(0)

        response = self.client.post(
            path=self.url,
            content_type=MULTIPART_CONTENT,
            data=encode_multipart(
                data={
                    "image": image_file,
                    "resource_type": "photo_booth",
                    "resource_type_id": "1",
                },
                boundary=BOUNDARY,
            ),
        )

        assert response.status_code == 401

    def test_image_upload_fail_blank_field(self, new_users, mocker):
        mocker.patch("django.core.files.storage.default_storage.save")

        temp_file = tempfile.NamedTemporaryFile()
        temp_file.name = "image.png"
        image_file = self.get_temporary_image(temp_file)
        image_file.seek(0)

        access_token = self.obtain_token(new_users)
        self.authenticate_with_token(access_token)

        response = self.client.post(
            path=self.url,
            content_type=MULTIPART_CONTENT,
            data=encode_multipart(
                data={
                    "image": image_file,
                    "resource_type": "",
                    "resource_type_id": "1",
                },
                boundary=BOUNDARY,
            ),
        )
        assert response.status_code == 400

    def test_image_upload_fail_required_field(self, new_users, mocker):
        mocker.patch("django.core.files.storage.default_storage.save")

        temp_file = tempfile.NamedTemporaryFile()
        temp_file.name = "image.png"
        image_file = self.get_temporary_image(temp_file)
        image_file.seek(0)

        access_token = self.obtain_token(new_users)
        self.authenticate_with_token(access_token)

        response = self.client.post(
            path=self.url,
            content_type=MULTIPART_CONTENT,
            data=encode_multipart(
                data={
                    "image": image_file,
                    "resource_type_id": "1",
                },
                boundary=BOUNDARY,
            ),
        )
        assert response.status_code == 400
