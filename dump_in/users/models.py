from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from dump_in.common.base.models import BaseModel, SimpleModel
from dump_in.users.managers import UserManager


class GenderChoices(models.TextChoices):
    MALE = "M", "Male"
    FEMALE = "F", "Female"


class User(AbstractBaseUser, BaseModel, PermissionsMixin):
    email = models.EmailField()
    username = models.CharField(max_length=128, unique=True)
    nickname = models.CharField(max_length=64, unique=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True)
    is_agree_privacy = models.BooleanField(default=True)
    is_agree_marketing = models.BooleanField(default=False)
    gender = models.CharField(max_length=1, choices=GenderChoices.choices, null=True, blank=True)
    birth = models.DateField(null=True)
    user_social_provider = models.ForeignKey(
        "UserSocialProvider",
        on_delete=models.SET_NULL,
        null=True,
        related_name="users",
    )

    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email", "nickname"]

    def __str__(self):
        return f"[{self.id}]: {self.email}"

    @property
    def is_staff(self):
        return self.is_admin

    class Meta:
        db_table = "user"


class UserSocialProvider(SimpleModel):
    """
    # apple: 애플 제공자
    # naver: 네이버 제공자
    # kakao: 카카오 제공자
    # email: 이메일 제공자
    """

    def __str__(self):
        return f"[{self.id}]: {self.name}"

    class Meta:
        db_table = "user_social_provider"
        verbose_name = "user social provider"
        verbose_name_plural = "user social providers"


class UserMobileToken(BaseModel):
    user = models.ForeignKey(
        "User",
        on_delete=models.SET_NULL,
        null=True,
        related_name="mobile_tokens",
    )
    token = models.CharField(max_length=512, unique=True)

    def __str__(self):
        return f"[{self.id}]: {self.user_id}"

    class Meta:
        db_table = "user_mobile_token"
        verbose_name = "user mobile token"
        verbose_name_plural = "user mobile tokens"


class Notification(BaseModel):
    title = models.CharField(max_length=64)
    content = models.CharField(max_length=128)
    is_read = models.BooleanField(default=False)
    parameter_data = models.CharField(max_length=512, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey("NotificationCategory", on_delete=models.CASCADE)

    def __str__(self):
        return f"[{self.id}/{self.user}] {self.title}"

    class Meta:
        db_table = "notification"
        verbose_name = "notification"
        verbose_name_plural = "notifications"


class NotificationCategory(SimpleModel):
    def __str__(self):
        return self.name

    class Meta:
        db_table = "notification_category"
        verbose_name = "notification category"
        verbose_name_plural = "notification categories"
