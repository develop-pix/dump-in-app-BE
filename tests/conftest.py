from datetime import timedelta

import pytest
from django.utils import timezone
from rest_framework.test import APIClient

from dump_in.users.models import User
from tests.factories import (
    ConceptFactory,
    GroupFactory,
    PhotoBoothBrandFactory,
    PhotoBoothFactory,
    ReviewFactory,
    ReviewImageFactory,
    UserSocialProviderFactory,
)


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
    return UserSocialProviderFactory.create_batch(4)


@pytest.fixture
def group(db):
    return GroupFactory.create_batch(3)


@pytest.fixture
def photo_booth_brand(db):
    return PhotoBoothBrandFactory.create_batch(3)


@pytest.fixture
def photo_booth(db):
    return PhotoBoothFactory()


@pytest.fixture()
def review(db):
    return ReviewFactory()


@pytest.fixture()
def review_list(db):
    concept = ConceptFactory(
        id=1,
        name="test",
    )

    ReviewFactory.create_batch(
        size=3,
        frame_color="red",
        participants="1",
        camera_shot="red1",
        concepts=[concept],
    )

    ReviewFactory.create_batch(
        size=4,
        frame_color="blue",
        participants="2",
        camera_shot="blue2",
    )


@pytest.fixture()
def review_image(db):
    return ReviewImageFactory()


@pytest.fixture()
def concept(db):
    return ConceptFactory(
        id=1,
    )
