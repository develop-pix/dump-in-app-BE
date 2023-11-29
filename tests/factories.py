import random
from datetime import datetime

import factory
from django.contrib.auth.models import Group
from faker import Faker

from dump_in.photo_booths.models import PhotoBooth
from dump_in.reviews.models import HashTag, Review, ReviewImage
from dump_in.users.models import User, UserSocialProvider

faker = Faker()


class UserSocialProviderFactory(factory.django.DjangoModelFactory):
    id = factory.Iterator(range(1, 5))
    name = factory.Iterator(["kakao", "naver", "apple", "email"])
    description = factory.LazyAttribute(lambda _: faker.text(max_nb_chars=128))

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
    gender = faker.random_element(elements=("M", "F"))
    birth = faker.date()

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


class PhotoBoothFactory(factory.django.DjangoModelFactory):
    id = factory.Sequence(lambda n: n)
    created_at = datetime.now()
    updated_at = datetime.now()

    class Meta:
        model = PhotoBooth


class HashTagFactory(factory.django.DjangoModelFactory):
    id = factory.Sequence(lambda n: n)
    name = factory.Sequence(lambda n: f"hash{n}")

    class Meta:
        model = HashTag


class ReviewFactory(factory.django.DjangoModelFactory):
    content = faker.text()
    is_deleted = False
    date = faker.date()
    frame_color = factory.LazyAttribute(lambda _: faker.text(max_nb_chars=8))
    participants = factory.LazyAttribute(lambda _: random.randint(1, 6))
    camera_shot = factory.LazyAttribute(lambda _: faker.text(max_nb_chars=8))
    goods_amount = faker.pybool()
    curl_amount = faker.pybool()
    is_public = True
    view_count = faker.random_number()
    like_count = faker.random_number()
    user = factory.SubFactory(UserFactory)
    photo_booth = factory.SubFactory(PhotoBoothFactory)

    class Meta:
        model = Review

    @factory.post_generation
    def hashtags(self, create, extracted, **kwargs):
        if extracted:
            for hashtag in extracted:
                self.hashtags.add(hashtag)

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
