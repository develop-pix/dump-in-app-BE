from config.env import env
from config.django.base import *  # noqa

DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "NAME": env("LOCAL_POSTGRESQL_DATABASE", default="dump_in"),
        "USER": env("LOCAL_POSTGRESQL_USER", default="postgres"),
        "PASSWORD": env("LOCAL_POSTGRESQL_PASSWORD", default="password"),
        "HOST": env("LOCAL_POSTGRESQL_HOST", default="localhost"),
        "PORT": env("LOCAL_POSTGRESQL_PORT", default="5432"),
    }
}

GEOS_LIBRARY_PATH = env.str("GEOS_LIBRARY_PATH")
GDAL_LIBRARY_PATH = env.str("GDAL_LIBRARY_PATH")
