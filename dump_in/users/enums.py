from enum import Enum


class UserProvider(Enum):
    KAKAO = 1
    NAVER = 2
    APPLE = 3
    EMAIL = 4


class AuthGroup(Enum):
    NORMAL_USER = 1
    ADMIN = 2
    SUPER_USER = 3
