from django.db import models

from dump_in.common.base.models import BaseModel, SimpleModel
from dump_in.photo_booths.models import PhotoBooth
from dump_in.users.models import User


class Concept(SimpleModel):
    def __str__(self):
        return f"[{self.id}]: {self.name}"

    class Meta:
        db_table = "concept"
        verbose_name = "concept"
        verbose_name_plural = "concepts"


class Review(BaseModel):
    content = models.TextField()
    main_thumbnail_image_url = models.URLField(max_length=512)
    date = models.DateField()
    frame_color = models.CharField(max_length=8)
    participants = models.IntegerField()
    camera_shot = models.CharField(max_length=8)
    goods_amount = models.BooleanField(null=True)
    curl_amount = models.BooleanField(null=True)
    is_public = models.BooleanField(default=False)
    view_count = models.PositiveIntegerField(default=0)
    like_count = models.PositiveIntegerField(default=0)
    concept = models.ManyToManyField(Concept, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    photo_booth = models.ForeignKey(PhotoBooth, on_delete=models.CASCADE, related_name="reviews")
    user_review_like_logs = models.ManyToManyField(User, through="UserReviewLikeLog", related_name="review_like_logs")

    def __str__(self):
        return f"[{self.id}]: {self.content}"

    class Meta:
        db_table = "review"
        verbose_name = "review"
        verbose_name_plural = "reviews"


class ReviewImage(BaseModel):
    review_image_url = models.URLField(max_length=512)
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name="review_image")

    def __str__(self):
        return f"[{self.id}]: {self.review_image_url}"

    class Meta:
        db_table = "review_image"
        verbose_name = "review image"
        verbose_name_plural = "review images"


class UserReviewLikeLog(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review = models.ForeignKey(Review, on_delete=models.CASCADE)

    def __str__(self):
        return f"[{self.id}]: {self.user} - {self.review}"

    class Meta:
        db_table = "user_review_like_log"
        verbose_name = "user review like log"
        verbose_name_plural = "user review like logs"
