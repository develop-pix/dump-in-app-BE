from datetime import timedelta

import pytest
from django.contrib.auth.models import Group
from django.utils import timezone
from rest_framework.test import APIClient, APIRequestFactory

from dump_in.users.models import User, UserSocialProvider


@pytest.fixture
def api_factory():
    return APIRequestFactory()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def new_users(db):
    for i in range(1, 11):
        User.objects.create(
            id=i,
            email=f"test{i}@test.com",
            username=f"test{i}",
            nickname=f"test{i}",
        )
    user = User.objects.create(
        id=11,
        email="test11@test.com",
        username="test11",
        nickname="test11",
    )
    return user


@pytest.fixture
def deleted_users(db):
    user = User.objects.create(
        id=12,
        email="test12@test.com",
        username="test12",
        nickname="test12",
        is_deleted=True,
        deleted_at=timezone.now() - timedelta(days=20),
    )
    return user


@pytest.fixture
def not_active_users(db):
    user = User.objects.create(
        id=13,
        email="test13@test,com",
        username="test13",
        nickname="test13",
        is_active=False,
    )
    return user


@pytest.fixture
def user_social_provider(db):
    kakao_provider = UserSocialProvider.objects.create(
        id=1,
        name="kakao",
    )
    naver_provider = UserSocialProvider.objects.create(
        id=2,
        name="naver",
    )
    apple_provider = UserSocialProvider.objects.create(
        id=3,
        name="apple",
    )
    email_provider = UserSocialProvider.objects.create(
        id=4,
        name="email",
    )
    return kakao_provider, naver_provider, apple_provider, email_provider


@pytest.fixture
def group(db):
    normal_group = Group.objects.create(
        id=1,
        name="normal_user",
    )
    admin_group = Group.objects.create(
        id=2,
        name="admin",
    )
    super_group = Group.objects.create(
        id=3,
        name="super",
    )
    return admin_group, normal_group, super_group
