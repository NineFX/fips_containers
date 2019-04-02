FROM ish512/fips-go:1.0-alpine AS build
WORKDIR /
RUN set -eux; \
    apk add --no-cache \
        ca-certificates \
        linux-headers \
        curl \
        git \
        gcc \
        g++ \
        make \
        cmake \
        perl \
        tar \
        xz; \
    curl -O https://commondatastorage.googleapis.com/chromium-boringssl-docs/fips/boringssl-24e5886c0edfc409c8083d10f9f1120111efd6f5.tar.xz; \
    tar -xvf boringssl-24e5886c0edfc409c8083d10f9f1120111efd6f5.tar.xz; \
    mv boringssl boringssl-24e5886c0edfc409c8083d10f9f1120111efd6f5; \
    cd boringssl-24e5886c0edfc409c8083d10f9f1120111efd6f5; \
    mkdir build; \
    cd build; \
    cmake ..; \
    make; \
    cd ..; \
    go run util/all_tests.go
        
FROM alpine:latest
RUN set -eux; \
    apk add --no-cache ca-certificates
COPY --from=build /boringssl-24e5886c0edfc409c8083d10f9f1120111efd6f5 .
WORKDIR /boringssl-24e5886c0edfc409c8083d10f9f1120111efd6f5