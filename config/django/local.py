from config.env import env
from config.django.base import *  # noqa

DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "NAME": env("POSTGRESQL_DATABASE", default="dump_in"),
        "USER": env("POSTGRESQL_USER", default="postgres"),
        "PASSWORD": env("POSTGRESQL_PASSWORD", default="password"),
        "HOST": env("POSTGRESQL_HOST", default="localhost"),
        "PORT": env("POSTGRESQL_PORT", default="5432"),
    }
}

GEOS_LIBRARY_PATH = env.str("GEOS_LIBRARY_PATH")
GDAL_LIBRARY_PATH = env.str("GDAL_LIBRARY_PATH")
