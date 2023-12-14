from typing import List, Optional

from django.contrib.gis.db.models import PointField
from django.db import models

from dump_in.common.base.models import BaseModel, SimpleModel
from dump_in.users.models import User


class PhotoBoothBrand(SimpleModel):
    photo_booth_url = models.URLField(max_length=128)
    main_thumbnail_image_url = models.URLField(max_length=512, null=True)
    logo_image_url = models.URLField(max_length=512, null=True)
    is_event = models.BooleanField(default=False)
    hashtag = models.ManyToManyField("Hashtag", related_name="photo_booth_brands")

    def __str__(self):
        return f"[{self.id}] {self.name}"

    class Meta:
        db_table = "photo_booth_brand"
        verbose_name = "photo booth brand"
        verbose_name_plural = "photo booth brands"


class PhotoBooth(BaseModel):
    id = models.UUIDField(primary_key=True, editable=False)
    location = models.CharField(max_length=32)
    name = models.CharField(max_length=64)
    latitude = models.DecimalField(max_digits=13, decimal_places=10)
    longitude = models.DecimalField(max_digits=13, decimal_places=10)
    point = PointField(null=True)
    street_address = models.CharField(max_length=64)
    road_address = models.CharField(max_length=64)
    operation_time = models.CharField(max_length=64)
    like_count = models.PositiveIntegerField(default=0)
    view_count = models.PositiveIntegerField(default=0)
    photo_booth_brand = models.ForeignKey(PhotoBoothBrand, on_delete=models.SET_NULL, null=True)
    user_photo_booth_like_logs = models.ManyToManyField(User, through="UserPhotoBoothLikeLog", related_name="photo_booth_like_logs")
    photo_booth_brand_image = Optional[List[str]]

    def __str__(self):
        return f"[{self.id}] {self.name}"

    class Meta:
        db_table = "photo_booth"
        verbose_name = "photo booth"
        verbose_name_plural = "photo booths"


class PhotoBoothBrandImage(BaseModel):
    photo_booth_brand = models.ForeignKey(PhotoBoothBrand, on_delete=models.CASCADE, related_name="photo_booth_brand_image")
    photo_booth_brand_image_url = models.URLField(max_length=512)

    def __str__(self):
        return f"[{self.id}] {self.photo_booth_brand_image_url}"

    class Meta:
        db_table = "photo_booth_brand_image"
        verbose_name = "photo booth brand image"
        verbose_name_plural = "photo booth brand images"


class UserPhotoBoothLikeLog(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    photo_booth = models.ForeignKey(PhotoBooth, on_delete=models.CASCADE)

    def __str__(self):
        return f"[{self.id}] {self.user} - {self.photo_booth}"

    class Meta:
        db_table = "user_photo_booth_like_log"
        verbose_name = "user photo booth like log"
        verbose_name_plural = "user photo booth like logs"


class Hashtag(SimpleModel):
    def __str__(self):
        return f"[{self.id}] {self.name}"

    class Meta:
        db_table = "hashtag"
        verbose_name = "hashtag"
        verbose_name_plural = "hashtags"
