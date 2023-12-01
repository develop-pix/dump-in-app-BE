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
    id = factory.Sequence(lambda n: n + 13)
    email = factory.LazyAttribute(lambda _: faker.unique.email())
    username = factory.LazyAttribute(lambda _: faker.unique.user_name())
    nickname = factory.LazyAttribute(lambda _: faker.unique.user_name())
    is_active = True
    is_deleted = faker.pybool()
    is_admin = faker.pybool()
    is_agree_privacy = True
    is_agree_marketing = faker.pybool()
    gender = FuzzyChoice(choices=["M", "F"])
    birth = FuzzyDate(start_date=datetime(1990, 1, 1), end_date=datetime(2000, 12, 31))

    class Meta:
        model = User

    @factory.post_generation
    def deleted_at(self, create, extracted, **kwargs):
        if not self.is_deleted:
            self.deleted_at = None
        else:
            self.deleted_at = faker.date()

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
    is_event = faker.pybool()
    # category = factory.LazyAttribute(lambda _: faker.text(max_nb_chars=64))

    class Meta:
        model = PhotoBoothBrand


class PhotoBoothFactory(factory.django.DjangoModelFactory):
    id = factory.LazyAttribute(lambda _: faker.uuid4())
    name = FuzzyText(length=64)
    latitude = faker.latitude()
    longitude = faker.longitude()
    street_address = FuzzyText(length=64)
    road_address = FuzzyText(length=64)
    operating_time = FuzzyText(length=64)
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
    is_deleted = False
    date = faker.date()
    frame_color = faker.color()
    participants = FuzzyInteger(low=0, high=6)
    camera_shot = FuzzyText(length=8)
    goods_amount = faker.pybool()
    curl_amount = faker.pybool()
    is_public = True
    like_count = FuzzyInteger(low=0, high=1000)
    view_count = FuzzyInteger(low=0, high=1000)
    user = factory.SubFactory(UserFactory)
    photo_booth = factory.SubFactory(PhotoBoothFactory)

    class Meta:
        model = Review

    @factory.post_generation
    def concepts(self, create, extracted, **kwargs):
        if extracted:
            for concept in extracted:
                self.concepts.add(concept)

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
