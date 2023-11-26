from config.env import env

KAKAO_SECRET_KEY = env.str("KAKAO_SECRET_KEY", default=None)
KAKAO_API_KEY = env.str("KAKAO_API_KEY", default=None)

NAVER_CLIENT_SECRET = env.str("NAVER_CLIENT_SECRET", default=None)
NAVER_CLIENT_ID = env.str("NAVER_CLIENT_ID", default=None)

APPLE_TEAM_ID = env.str("APPLE_TEAM_ID", default=None)
APPLE_CLIENT_ID = env.str("APPLE_CLIENT_ID", default=None)
APPLE_KEY_ID = env.str("APPLE_KEY_ID", default=None)
APPLE_PRIVATE_KEY = env.str("APPLE_PRIVATE_KEY", default=None)
