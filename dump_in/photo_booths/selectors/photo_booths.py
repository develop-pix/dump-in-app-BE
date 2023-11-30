from typing import Optional

from dump_in.photo_booths.models import PhotoBooth


class PhotoBoothSelector:
    def get_photo_booth_by_id(self, photo_booth_id: str) -> Optional[PhotoBooth]:
        try:
            return PhotoBooth.objects.filter(id=photo_booth_id).get()
        except PhotoBooth.DoesNotExist:
            return None
