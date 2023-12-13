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
    UserFactory,
    UserSocialProviderFactory,
)


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user_social_provider(db):
    return UserSocialProviderFactory.create_batch(4)


@pytest.fixture
def group(db):
    return GroupFactory.create_batch(3)


@pytest.fixture
def valid_user(db):
    return User.objects.create(
        id=1,
        email="test1@test.com",
        username="test1",
        nickname="test1",
        is_deleted=False,
        is_admin=False,
        is_active=True,
    )


@pytest.fixture
def valid_user_list(db):
    return UserFactory.create_batch(11)


@pytest.fixture
def deleted_user(db):
    return User.objects.create(
        id=2,
        email="test2@test.com",
        username="test2",
        nickname="test2",
        deleted_at=timezone.now() - timezone.timedelta(days=14),
        is_deleted=True,
        is_admin=False,
        is_active=True,
    )


@pytest.fixture
def inactive_user(db):
    return User.objects.create(
        id=3,
        email="test3@test.com",
        username="test3",
        nickname="test3",
        is_deleted=False,
        is_admin=False,
        is_active=False,
    )


@pytest.fixture
def photo_booth_brand_list(db):
    return PhotoBoothBrandFactory.create_batch(3)


@pytest.fixture
def photo_booth(db):
    return PhotoBoothFactory()


@pytest.fixture
def photo_booth_list(db):
    photo_booth_brand = PhotoBoothBrandFactory()

    return PhotoBoothFactory.create_batch(size=100, photo_booth_brand=photo_booth_brand)


@pytest.fixture
def concept(db):
    return ConceptFactory(id=1)


@pytest.fixture
def concept_list(db):
    return ConceptFactory.create_batch(10)


@pytest.fixture
def valid_review(db):
    return ReviewFactory()


@pytest.fixture
def valid_review_list(db):
    return ReviewFactory.create_batch(10)


@pytest.fixture
def valid_review_list_photo_booth_location(db):
    photo_booth = PhotoBoothFactory(location="강남")
    return ReviewFactory.create_batch(3, photo_booth=photo_booth)


@pytest.fixture
def valid_review_list_frame_color(db):
    return ReviewFactory.create_batch(3, frame_color="red")


@pytest.fixture
def valid_review_list_participants(db):
    return ReviewFactory.create_batch(3, participants=1)


@pytest.fixture
def valid_review_list_camera_shot(db):
    return ReviewFactory.create_batch(3, camera_shot="front")


@pytest.fixture
def valid_review_list_concept(db):
    concept = ConceptFactory()
    return ReviewFactory.create_batch(3, concept=[concept])


@pytest.fixture
def valid_review_bulk(db):
    photo_booth = PhotoBoothFactory()
    concept_list = ConceptFactory.create_batch(30)
    review_list = ReviewFactory.create_batch(size=100, photo_booth=photo_booth, concept=concept_list)

    for review in review_list:
        ReviewImageFactory.create_batch(5, review=review)

    return review_list


@pytest.fixture
def valid_review_list_by_valid_user(db, valid_user):
    return ReviewFactory.create_batch(10, user=valid_user)


@pytest.fixture
def deleted_review(db):
    return ReviewFactory(is_deleted=True)


@pytest.fixture
def private_review(db):
    return ReviewFactory(is_public=False)


@pytest.fixture
def review_image(db):
    return ReviewImageFactory()
