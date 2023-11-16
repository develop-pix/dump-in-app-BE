from django.contrib.auth.models import BaseUserManager

from dump_in.common.constants import (
    AUTH_GROUP_ADMIN,
    AUTH_GROUP_NORMAL_USER,
    AUTH_GROUP_SUPER_USER,
    USER_SOCIAL_PROVIDER_EMAIL,
)


class UserManager(BaseUserManager):
    def create_social_user(self, email: str, nickname: str, social_id: str, social_provider: int, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(
            username=social_id,
            email=email,
            nickname=nickname,
            user_social_provider_id=social_provider,
            **extra_fields,
        )
        user.set_unusable_password()
        user.save(using=self._db)
        user.groups.add(AUTH_GROUP_NORMAL_USER)
        return user

    def create_superuser(self, email: str, username: str, password: str, nickname: str, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(
            username=username,
            email=email,
            nickname=nickname,
            is_superuser=True,
            is_admin=True,
            user_social_provider_id=USER_SOCIAL_PROVIDER_EMAIL,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        user.groups.add(AUTH_GROUP_SUPER_USER)
        return user

    def create_admin(self, email: str, username: str, password: str, nickname: str, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(
            username=username,
            email=email,
            nickname=nickname,
            is_admin=True,
            user_social_provider_id=USER_SOCIAL_PROVIDER_EMAIL,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        user.groups.add(AUTH_GROUP_ADMIN)
        return user
