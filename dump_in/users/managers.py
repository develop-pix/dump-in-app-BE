from django.contrib.auth.models import BaseUserManager

from dump_in.users.enums import AuthGroup, UserProvider


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
        user.groups.add(AuthGroup.NORMAL_USER.value)
        return user

    def create_superuser(self, email: str, username: str, password: str, nickname: str, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(
            username=username,
            email=email,
            nickname=nickname,
            is_superuser=True,
            is_admin=True,
            user_social_provider_id=UserProvider.EMAIL.value,
            **extra_fields,
        )
        user.set_password(password)

        user.save(using=self._db)
        user.groups.add(AuthGroup.SUPER_USER.value)
        return user

    def create_admin(self, email: str, username: str, password: str, nickname: str, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(
            username=username,
            email=email,
            nickname=nickname,
            is_admin=True,
            user_social_provider_id=UserProvider.EMAIL.value,
            **extra_fields,
        )
        user.set_password(password)

        user.save(using=self._db)
        user.groups.add(AuthGroup.ADMIN.value)
        return user
