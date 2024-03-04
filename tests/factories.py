import json
from datetime import datetime

import factory
import pytz
from django.contrib.auth.models import Group
from factory.fuzzy import FuzzyChoice, FuzzyDate, FuzzyDateTime, FuzzyInteger, FuzzyText
from faker import Faker

from dump_in.events.enums import EventHashtag
from dump_in.events.models import Event, EventImage
from dump_in.photo_booths.enums import PhotoBoothLocation
from dump_in.photo_booths.models import (
    Hashtag,
    PhotoBooth,
    PhotoBoothBrand,
    PhotoBoothBrandImage,
)
from dump_in.reviews.enums import CameraShot
from dump_in.reviews.enums import Concept as ConceptEnum
from dump_in.reviews.enums import FrameColor
from dump_in.reviews.models import Concept, Review, ReviewImage
from dump_in.users.models import (
    Notification,
    NotificationCategory,
    User,
    UserMobileToken,
    UserSocialProvider,
)

faker = Faker("ko_KR")


class UserSocialProviderFactory(factory.django.DjangoModelFactory):
    id = factory.Iterator(range(1, 5))
    name = factory.Iterator(["kakao", "naver", "apple", "email"])
    description = FuzzyText(length=128)

    class Meta:
        model = UserSocialProvider


class GroupFactory(factory.django.DjangoModelFactory):
    id = factory.Iterator(range(1, 4))
    name = factory.Iterator(["normal_user", "admin", "super_admin"])

    class Meta:
        model = Group


class UserFactory(factory.django.DjangoModelFactory):
    id = factory.Sequence(lambda n: n + 10)
    email = factory.LazyAttribute(lambda _: faker.unique.email())
    username = FuzzyText(length=16)
    nickname = factory.LazyAttribute(lambda _: faker.unique.user_name())
    is_agree_privacy = True
    is_agree_marketing = faker.pybool()
    gender = FuzzyChoice(choices=["M", "F"])
    birth = FuzzyDate(start_date=datetime(1990, 1, 1), end_date=datetime(2000, 12, 31))

    class Meta:
        model = User

    @factory.post_generation
    def deleted_at(self, create, extracted, **kwargs):
        if isinstance(extracted, datetime):
            self.deleted_at = extracted
        else:
            self.deleted_at = None

    @factory.post_generation
    def is_deleted(self, create, extracted, **kwargs):
        if isinstance(extracted, bool):
            self.is_deleted = extracted
        else:
            self.is_deleted = False

    @factory.post_generation
    def is_admin(self, create, extracted, **kwargs):
        if isinstance(extracted, bool):
            self.is_admin = extracted
        else:
            self.is_admin = False

    @factory.post_generation
    def is_active(self, create, extracted, **kwargs):
        if isinstance(extracted, bool):
            self.is_active = extracted
        else:
            self.is_active = True

    @factory.post_generation
    def groups(self, create, extracted, **kwargs):
        if extracted:
            for group in extracted:
                self.groups.add(group)


class UserMobileTokenFactory(factory.django.DjangoModelFactory):
    id = factory.Sequence(lambda n: n)
    token = factory.LazyAttribute(lambda _: faker.unique.uuid4())
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = UserMobileToken


class NotificationCategoryFactory(factory.django.DjangoModelFactory):
    id = factory.Sequence(lambda n: n)
    name = factory.Sequence(lambda n: f"notification_category{n}")

    class Meta:
        model = NotificationCategory


class NotificationFactory(factory.django.DjangoModelFactory):
    title = FuzzyText(length=64)
    content = FuzzyText(length=128)
    parameter_data = FuzzyText(length=512)
    user = factory.SubFactory(UserFactory)
    category = factory.SubFactory(NotificationCategoryFactory)

    class Meta:
        model = Notification

    @factory.post_generation
    def is_read(self, create, extracted, **kwargs):
        if isinstance(extracted, bool):
            self.is_read = extracted
        else:
            self.is_read = False

    @factory.post_generation
    def is_deleted(self, create, extracted, **kwargs):
        if isinstance(extracted, bool):
            self.is_deleted = extracted
        else:
            self.is_deleted = False


class HashtagFactory(factory.django.DjangoModelFactory):
    id = factory.Sequence(lambda n: n)
    name = factory.Iterator([hashtag.value for hashtag in EventHashtag])

    class Meta:
        model = Hashtag


class PhotoBoothBrandFactory(factory.django.DjangoModelFactory):
    id = factory.Sequence(lambda n: n)
    name = faker.text(max_nb_chars=64)
    description = FuzzyText(length=128)
    photo_booth_url = faker.url()
    main_thumbnail_image_url = faker.image_url()
    logo_image_url = faker.image_url()

    class Meta:
        model = PhotoBoothBrand

    @factory.post_generation
    def is_event(self, create, extracted, **kwargs):
        if isinstance(extracted, bool):
            self.is_event = extracted
        else:
            self.is_event = False

    @factory.post_generation
    def hashtag(self, create, extracted, **kwargs):
        if extracted:
            for hashtag in extracted:
                self.hashtag.add(hashtag)

    @factory.post_generation
    def photo_booth_brand_image(self, create, extracted, **kwargs):
        if extracted:
            for photo_booth_brand_image in extracted:
                self.photo_booth_brand_image.add(photo_booth_brand_image)


class PhotoBoothBrandImageFactory(factory.django.DjangoModelFactory):
    photo_booth_brand_image_url = faker.image_url()
    photo_booth_brand = factory.SubFactory(PhotoBoothBrandFactory)

    class Meta:
        model = PhotoBoothBrandImage


class PhotoBoothFactory(factory.django.DjangoModelFactory):
    id = factory.LazyAttribute(lambda _: faker.uuid4())
    name = FuzzyText(length=64)
    location = FuzzyChoice([location.value for location in PhotoBoothLocation])
    latitude = faker.latitude()
    longitude = faker.longitude()
    point = factory.LazyAttribute(
        lambda _: json.dumps(
            {
                "type": "Point",
                "coordinates": [126.97061201527232, 37.55466577566926],
            }
        )
    )  # 서울역
    street_address = FuzzyText(length=64)
    road_address = FuzzyText(length=64)
    operation_time = FuzzyText(length=64)
    like_count = FuzzyInteger(low=0, high=1000)
    view_count = FuzzyInteger(low=0, high=1000)
    photo_booth_brand = factory.SubFactory(PhotoBoothBrandFactory)
    created_at = FuzzyDateTime(datetime(2023, 11, 11, tzinfo=pytz.timezone("Asia/Seoul")))
    updated_at = FuzzyDateTime(datetime(2023, 11, 11, tzinfo=pytz.timezone("Asia/Seoul")))

    class Meta:
        model = PhotoBooth


class ConceptFactory(factory.django.DjangoModelFactory):
    id = factory.Sequence(lambda n: n)
    name = factory.Iterator([concept.value for concept in ConceptEnum])

    class Meta:
        model = Concept


class ReviewFactory(factory.django.DjangoModelFactory):
    content = faker.text()
    main_thumbnail_image_url = faker.image_url()
    date = faker.date()
    frame_color = FuzzyChoice([color.value for color in FrameColor])
    participants = FuzzyInteger(low=0, high=5)
    camera_shot = FuzzyChoice([shot.value for shot in CameraShot])
    goods_amount = faker.pybool()
    curl_amount = faker.pybool()
    like_count = FuzzyInteger(low=0, high=1000)
    view_count = FuzzyInteger(low=0, high=1000)
    photo_booth = factory.SubFactory(PhotoBoothFactory)
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = Review

    @factory.post_generation
    def is_deleted(self, create, extracted, **kwargs):
        if isinstance(extracted, bool):
            self.is_deleted = extracted
        else:
            self.is_deleted = False

    @factory.post_generation
    def is_public(self, create, extracted, **kwargs):
        if isinstance(extracted, bool):
            self.is_public = extracted
        else:
            self.is_public = True

    @factory.post_generation
    def concept(self, create, extracted, **kwargs):
        if extracted:
            for concept in extracted:
                self.concept.add(concept)

    @factory.post_generation
    def user_review_like_logs(self, create, extracted, **kwargs):
        if extracted:
            for user in extracted:
                self.user_review_like_logs.add(user)


class ReviewImageFactory(factory.django.DjangoModelFactory):
    review_image_url = faker.image_url()
    review = factory.SubFactory(ReviewFactory)

    class Meta:
        model = ReviewImage


class EventFactory(factory.django.DjangoModelFactory):
    id = factory.Sequence(lambda n: n)
    title = FuzzyText(length=128)
    content = FuzzyText(length=256)
    main_thumbnail_image_url = faker.image_url()
    view_count = FuzzyInteger(low=0, high=1000)
    like_count = FuzzyInteger(low=0, high=1000)
    start_date = FuzzyDateTime(datetime(2023, 11, 11, tzinfo=pytz.timezone("Asia/Seoul")))
    end_date = FuzzyDateTime(datetime(2023, 11, 30, tzinfo=pytz.timezone("Asia/Seoul")))
    photo_booth_brand = factory.SubFactory(PhotoBoothBrandFactory)
    created_at = FuzzyDateTime(datetime(2023, 11, 11, tzinfo=pytz.timezone("Asia/Seoul")))
    updated_at = FuzzyDateTime(datetime(2023, 11, 11, tzinfo=pytz.timezone("Asia/Seoul")))

    class Meta:
        model = Event

    @factory.post_generation
    def is_public(self, create, extracted, **kwargs):
        if isinstance(extracted, bool):
            self.is_public = extracted
        else:
            self.is_public = True

    @factory.post_generation
    def hashtag(self, create, extracted, **kwargs):
        if extracted:
            for hashtag in extracted:
                self.hashtag.add(hashtag)

    @factory.post_generation
    def user_event_like_logs(self, create, extracted, **kwargs):
        if extracted:
            for user in extracted:
                self.user_event_like_logs.add(user)

    @factory.post_generation
    def event_image(self, create, extracted, **kwargs):
        if extracted:
            for event_image in extracted:
                self.event_image.add(event_image)


class EventImageFactory(factory.django.DjangoModelFactory):
    event_image_url = faker.image_url()
    event = factory.SubFactory(EventFactory)

    class Meta:
        model = EventImage
