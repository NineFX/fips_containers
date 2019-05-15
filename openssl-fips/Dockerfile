FROM ubuntu:18.04 AS build

ENV OPENSSL openssl-fips-2.0.10

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

RUN set -eux; \
    apt-get -y update; \
    apt-get -y install \
        wget \
        xz-utils \
        gzip; \
    wget "https://www.openssl.org/source/openssl-fips-2.0.16.tar.gz"; \
    gunzip -c openssl-fips-2.0.16.tar.gz | tar xf -; \
    cd openssl-fips-2.0.16; \
    ## U2 command set
    ./config; \
    make; \
    make install