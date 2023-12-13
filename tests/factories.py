import json
from datetime import datetime

import factory
import pytz
from django.contrib.auth.models import Group
from factory.fuzzy import FuzzyChoice, FuzzyDate, FuzzyDateTime, FuzzyInteger, FuzzyText
from faker import Faker

from dump_in.photo_booths.models import PhotoBooth, PhotoBoothBrand
from dump_in.reviews.models import Concept, Review, ReviewImage
from dump_in.users.models import User, UserSocialProvider

faker = Faker()


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


class PhotoBoothBrandFactory(factory.django.DjangoModelFactory):
    id = factory.Sequence(lambda n: n)
    name = FuzzyText(length=64)
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


class PhotoBoothFactory(factory.django.DjangoModelFactory):
    id = factory.LazyAttribute(lambda _: faker.uuid4())
    name = FuzzyText(length=64)
    location = FuzzyText(length=32)
    latitude = faker.latitude()
    longitude = faker.longitude()
    point = factory.LazyAttribute(
        lambda _: json.dumps(
            {
                "type": "Point",
                "coordinates": [37.55466577566926, 126.97061201527232],
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
    name = factory.Sequence(lambda n: f"concept{n}")

    class Meta:
        model = Concept


class ReviewFactory(factory.django.DjangoModelFactory):
    content = faker.text()
    main_thumbnail_image_url = faker.image_url()
    date = faker.date()
    frame_color = faker.color()
    participants = FuzzyInteger(low=0, high=6)
    camera_shot = FuzzyText(length=8)
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
