from config.env import env

GEOS_LIBRARY_PATH = env.str("GEOS_LIBRARY_PATH", default="/usr/lib/aarch64-linux-gnu/libgeos_c.so.1.17.1")
GDAL_LIBRARY_PATH = env.str("GDAL_LIBRARY_PATH", default="/usr/lib/aarch64-linux-gnu/libgdal.so.32.3.6.2")
