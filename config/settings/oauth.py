from config.env import env

KAKAO_SECRET_KEY = env.str("KAKAO_SECRET_KEY", default=None)
KAKAO_API_KEY = env.str("KAKAO_API_KEY", default=None)

NAVER_CLIENT_SECRET = env.str("NAVER_CLIENT_SECRET", default=None)
NAVER_CLIENT_ID = env.str("NAVER_CLIENT_ID", default=None)
