import pytest
from django.utils import timezone
from rest_framework.test import APIClient

from tests.factories import (
    ConceptFactory,
    EventFactory,
    EventImageFactory,
    GroupFactory,
    HashtagFactory,
    NotificationFactory,
    PhotoBoothBrandFactory,
    PhotoBoothBrandImageFactory,
    PhotoBoothFactory,
    ReviewFactory,
    ReviewImageFactory,
    UserFactory,
    UserMobileTokenFactory,
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
    return UserFactory(
        is_deleted=False,
        is_admin=False,
        is_active=True,
    )


@pytest.fixture
def valid_user_list(db):
    return UserFactory.create_batch(11)


@pytest.fixture
def deleted_user(db):
    return UserFactory(
        deleted_at=timezone.now() - timezone.timedelta(days=14),
        is_deleted=True,
        is_admin=False,
        is_active=True,
    )


@pytest.fixture
def inactive_user(db):
    return UserFactory(
        is_deleted=False,
        is_admin=False,
        is_active=False,
    )


@pytest.fixture
def valid_user_mobile_token(db):
    return UserMobileTokenFactory()


@pytest.fixture
def valid_notification(db):
    return NotificationFactory()


@pytest.fixture
def valid_notification_list(db):
    user = UserFactory()

    return NotificationFactory.create_batch(
        size=10,
        user=user,
    )


@pytest.fixture
def read_notification(db):
    return NotificationFactory(is_read=True)


@pytest.fixture
def photo_booth_brand(db):
    photo_booth_brand_image = PhotoBoothBrandImageFactory()

    hashtag = HashtagFactory()

    return PhotoBoothBrandFactory(
        photo_booth_brand_image=[photo_booth_brand_image],
        hashtag=[hashtag],
    )


@pytest.fixture
def photo_booth_brand_list(db):
    return PhotoBoothBrandFactory.create_batch(3)


@pytest.fixture
def photo_booth_brand_image(db):
    return PhotoBoothBrandImageFactory()


@pytest.fixture
def photo_booth_brand_image_list(db):
    photo_booth_brand = PhotoBoothBrandFactory()

    return PhotoBoothBrandImageFactory.create_batch(
        size=10,
        photo_booth_brand=photo_booth_brand,
    )


@pytest.fixture
def photo_booth(db, photo_booth_brand):
    return PhotoBoothFactory(photo_booth_brand=photo_booth_brand)


@pytest.fixture
def photo_booth_list(db, photo_booth_brand):
    return PhotoBoothFactory.create_batch(size=10, photo_booth_brand=photo_booth_brand)


@pytest.fixture
def concept(db):
    return ConceptFactory()


@pytest.fixture
def concept_list(db):
    return ConceptFactory.create_batch(10)


@pytest.fixture
def valid_review(db):
    photo_booth_brand = PhotoBoothBrandFactory()

    photo_booth = PhotoBoothFactory(
        photo_booth_brand=photo_booth_brand,
    )

    concept = ConceptFactory()

    return ReviewFactory(
        photo_booth=photo_booth,
        concept=[concept],
    )


@pytest.fixture
def valid_review_list(db):
    photo_booth_brand = PhotoBoothBrandFactory()

    photo_booth = PhotoBoothFactory(
        photo_booth_brand=photo_booth_brand,
    )

    return ReviewFactory.create_batch(
        size=10,
        photo_booth=photo_booth,
    )


@pytest.fixture
def valid_review_list_photo_booth_location(db):
    photo_booth = PhotoBoothFactory(location="강남")
    return ReviewFactory.create_batch(3, photo_booth=photo_booth)


@pytest.fixture
def valid_review_list_frame_color(db):
    return ReviewFactory.create_batch(3, frame_color="#000000")


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
def valid_review_list_by_valid_user(db, valid_user):
    return ReviewFactory.create_batch(10, user=valid_user)


@pytest.fixture
def private_review(db):
    return ReviewFactory(is_public=False)


@pytest.fixture
def review_image(db):
    return ReviewImageFactory()


@pytest.fixture
def review_image_list(db):
    review = ReviewFactory()
    return ReviewImageFactory.create_batch(10, review=review)


@pytest.fixture
def valid_event(db):
    hashtag = HashtagFactory()
    evnet_image = EventImageFactory()

    photo_booth_brand = PhotoBoothBrandFactory(is_event=True)

    return EventFactory(
        photo_booth_brand=photo_booth_brand,
        hashtag=[hashtag],
        event_image=[evnet_image],
    )


@pytest.fixture
def private_event(db):
    return EventFactory(is_public=False)


@pytest.fixture
def valid_event_list(db):
    photo_booth_brand = PhotoBoothBrandFactory(is_event=True)

    return EventFactory.create_batch(
        size=10,
        photo_booth_brand=photo_booth_brand,
    )


@pytest.fixture
def invalid_event(db):
    photo_booth_brand = PhotoBoothBrandFactory(is_event=False)

    return EventFactory(photo_booth_brand=photo_booth_brand)
