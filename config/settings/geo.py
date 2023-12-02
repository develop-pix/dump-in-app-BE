from config.env import env


GEOS_LIBRARY_PATH = env.str("GEOS_LIBRARY_PATH", default="/usr/local/lib/libgeos_c.so")
GDAL_LIBRARY_PATH = env.str("GDAL_LIBRARY_PATH", default="/usr/local/lib/libgdal.so")
