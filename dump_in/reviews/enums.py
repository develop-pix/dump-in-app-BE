from enum import Enum


class FrameColor(Enum):
    BLACK = "#000000"
    WHITE = "#FFFFFF"
    BLUE = "#0072FF"
    RED = "#FF2E00"
    GREEN = "#00C868"
    YELLOW = "#FFE045"
    PURPLE = "#8F00FF"
    GRAY = "#A1A1A1"
    GRADIENT = "gradient"


class Participants(Enum):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5


class CameraShot(Enum):
    CLOSEUP = "클로즈업"
    UPPER_BODY = "상반신"
    KNEE = "무릎"
    FULL_BODY = "전신"


class Concept(Enum):
    DAILY = "일상"
    COUPLE = "커플"
    FRENDSHIP_SHOT = "우정샷"
    FAMILY = "가족"
    ANGLE = "앵글"
    COLLABO = "콜라보"
    CELEBRITY = "연예인"
    CHARACTER = "캐릭터"
    FRAME_OF_MONTH = "이달의 프레임"
    SEASON = "계절"
    BIRTHDAY = "생일"
    COMIC = "코믹"
    TRAVEL = "여행"
    HALLOWEEN = "할로윈"
    CHRISTMAS = "크리스마스"
    ETC = "기타"


class ReviewType(Enum):
    PHOTO_BOOTH_BRAND = "photo_booth_brand"
    PHOTO_BOOTH = "photo_booth"
    FILTER = "filter"
    SEARCH = "search"
