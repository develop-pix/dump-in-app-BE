FROM nginx:1.23.2

COPY ./nginx/default.conf /etc/nginx/conf.d/default.conf

RUN nginx -V 2>&1 | grep -q -- --with-http_geoip_module \
    || { \
        apt-get update \
        && apt-get install -y libnginx-mod-http-geoip geoip-database \
        && rm -rf /var/lib/apt/lists/*; \
    }

RUN [ -e /usr/share/GeoIP/GeoIP.dat ] || { \
        mkdir -p /usr/share/GeoIP \
        && cd /usr/share/GeoIP \
        && wget https://centminmod.com/centminmodparts/geoip-legacy/GeoIP.dat.gz \
        && gunzip GeoIP.dat.gz; \
    }
