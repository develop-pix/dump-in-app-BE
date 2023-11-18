import tempfile

import pytest
from PIL import Image

from dump_in.images.services import ImageUploadService

pytestmark = pytest.mark.django_db


class TestImageUploadService:
    def get_temporary_image(self):
        size = (100, 100)
        color = (255, 0, 0, 0)
        image = Image.new("RGBA", size, color)
        temp_file = tempfile.NamedTemporaryFile(suffix=".png")
        image.save(temp_file, "png")
        return temp_file

    def test_image_upload_success(self, new_users, mocker):
        mocker.patch("django.core.files.storage.default_storage.save")

        temp_file = self.get_temporary_image()

        service = ImageUploadService(
            image_obj=temp_file,
            resource_type="photo_booth",
            resource_type_id=1,
        )
        upload_path = service.upload_image()
        assert upload_path is not None

    def test_image_upload_fail_invalid_image_type(self, new_users, mocker):
        mocker.patch("django.core.files.storage.default_storage.save")

        temp_file = tempfile.NamedTemporaryFile(suffix=".txt")

        service = ImageUploadService(
            image_obj=temp_file,
            resource_type="photo_booth",
            resource_type_id=1,
        )
        with pytest.raises(Exception) as e:
            service.upload_image()

        assert e.value.status_code == 400

    def test_image_upload_fail_invalid_resource_type(self, new_users, mocker):
        mocker.patch("django.core.files.storage.default_storage.save")

        temp_file = self.get_temporary_image()

        service = ImageUploadService(
            image_obj=temp_file,
            resource_type="invalid_resource_type",
            resource_type_id=1,
        )
        with pytest.raises(Exception) as e:
            service.upload_image()

        assert str(e.value) == "Invalid resource type: invalid_resource_type"
        assert e.value.status_code == 400
