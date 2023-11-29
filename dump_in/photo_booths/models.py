from dump_in.common.base.models import BaseModel


class PhotoBooth(BaseModel):
    def __str__(self):
        return f"{self.id}"

    class Meta:
        db_table = "photo_booth"
        verbose_name = "photo booth"
        verbose_name_plural = "photo booths"