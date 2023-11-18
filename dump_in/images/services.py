from datetime import datetime

from django.conf import settings
from django.core.files.storage import default_storage
from PIL import Image

from dump_in.common.exception.exceptions import ValidationException
from dump_in.images.utils import bytes_to_mib


class ImageUploadService:
    def __init__(self, image_obj, resource_type: str, resource_type_id: int):
        self.resource_type_id = resource_type_id
        self.image_obj = image_obj
        self.resource_type = resource_type

    def _validate_image_size(self):
        max_size = settings.IMAGE_MAX_SIZE
        image_size = len(self.image_obj.read())

        if image_size > max_size:
            raise ValidationException(f"Image is too large. It should not exceed {bytes_to_mib(max_size)} MiB")

    def _validate_image_type(self):
        try:
            image = Image.open(self.image_obj)
            image.verify()

        except:
            raise ValidationException(f"Invalid image type")

    def _get_resource_path(self) -> str:
        id_path = str(self.resource_type_id)
        ext = str(self.image_obj.name).split(".")[-1]

        if self.resource_type == "photo_booth":
            resource_path = "photo_booths/" + id_path + "/" + datetime.now().strftime("%Y-%m-%d-%H-%M-%S.%f") + "." + ext
        elif self.resource_type == "review":
            resource_path = "reviews/" + id_path + "/" + datetime.now().strftime("%Y-%m-%d-%H-%M-%S.%f") + "." + ext
        elif self.resource_type == "event":
            resource_path = "events/" + id_path + "/" + datetime.now().strftime("%Y-%m-%d-%H-%M-%S.%f") + "." + ext
        else:
            raise ValidationException(f"Invalid resource type: {self.resource_type}")
        return resource_path

    def upload_image(self) -> str:
        try:
            self._validate_image_size()

            self._validate_image_type()

            upload_path = self._get_resource_path()

            default_storage.save(upload_path, self.image_obj)

            return settings.AWS_S3_URL + "/" + upload_path

        except Exception as e:
            raise ValidationException(str(e))
