from typing import Tuple

from django.db import transaction
from django.db.models import F

from dump_in.common.exception.exceptions import NotFoundException
from dump_in.photo_booths.models import PhotoBooth
from dump_in.photo_booths.selectors.photo_booths import PhotoBoothSelector


class PhotoBoothService:
    @transaction.atomic
    def like_photo_booth(self, photo_booth_id: str, user) -> Tuple[PhotoBooth, bool]:
        photo_booth_selector = PhotoBoothSelector()
        photo_booth = photo_booth_selector.get_photo_booth_by_id(photo_booth_id=photo_booth_id)

        if photo_booth is None:
            raise NotFoundException("Photo Booth does not exist")

        if photo_booth.user_photo_booth_like_logs.filter(id=user.id).exists():
            photo_booth.user_photo_booth_like_logs.remove(user)
            photo_booth.like_count = F("like_count") - 1
            is_liked = False

        else:
            photo_booth.user_photo_booth_like_logs.add(user)
            photo_booth.like_count = F("like_count") + 1
            is_liked = True

        photo_booth.save(update_fields=["like_count"])

        return photo_booth, is_liked
