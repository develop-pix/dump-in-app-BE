from django.db import models

from dump_in.common.base.models import BaseModel
from dump_in.photo_booths.models import Hashtag, PhotoBoothBrand
from dump_in.users.models import User


class Event(BaseModel):
    title = models.CharField(max_length=128)
    content = models.TextField()
    main_thumbnail_image_url = models.URLField()
    view_count = models.PositiveIntegerField(default=0)
    like_count = models.PositiveIntegerField(default=0)
    is_public = models.BooleanField(default=False)
    start_date = models.DateField()
    end_date = models.DateField()
    hashtag = models.ManyToManyField(Hashtag, related_name="events")
    photo_booth_brand = models.ForeignKey(PhotoBoothBrand, on_delete=models.CASCADE, related_name="events")
    user_event_like_logs = models.ManyToManyField(User, through="UserEventLikeLog", related_name="event_like_logs")

    def __str__(self):
        return f"[{self.id}]: {self.title}"

    class Meta:
        db_table = "event"
        verbose_name = "event"
        verbose_name_plural = "events"


class EventImage(BaseModel):
    event_image_url = models.URLField()
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="event_image")

    def __str__(self):
        return f"[{self.id}]: {self.event_image_url}"

    class Meta:
        db_table = "event_image"
        verbose_name = "event image"
        verbose_name_plural = "event images"


class UserEventLikeLog(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    def __str__(self):
        return f"[{self.id}]: {self.user} - {self.event}"

    class Meta:
        db_table = "user_event_like_log"
        verbose_name = "user event like log"
        verbose_name_plural = "user event like logs"
