from config.env import env


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("POSTGRESQL_DATABASE", default="dump-in"),
        "USER": env("POSTGRESQL_USER", default="postgres"),
        "PASSWORD": env("POSTGRESQL_PASSWORD", default="password"),
        "HOST": env("POSTGRESQL_HOST", default="localhost"),
        "PORT": env("POSTGRESQL_PORT", default="5432"),
    }
}

SESSION_COOKIE_SECURE = True
