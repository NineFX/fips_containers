FROM ish512/fips-go:1.0-ubuntu AS build
ENV BORINGCRYPTO_VERSION 20180730
WORKDIR /
RUN set -eux; \
    apt-get update -y && apt-get install -y \
        ca-certificates \
        gcc \
        g++ \
        make \
        cmake \
        git-core \
        perl; \
    git clone --single-branch --branch fips-${BORINGCRYPTO_VERSION} https://boringssl.googlesource.com/boringssl; \
    cd boringssl; \
    mkdir build; \
    cd build; \
    cmake ..; \
    make; \
    cd ..; \
    go run util/all_tests.go; \
    cd ssl/test/runner && go test

FROM ubuntu:latest
RUN set -eux; \
    apt-get update -y && apt-get install -y ca-certificates
COPY --from=build /boringssl .
WORKDIR /boringssl