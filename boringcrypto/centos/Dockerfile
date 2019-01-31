FROM ish512/fips-go:1.0-centos AS build
ENV BORINGCRYPTO_VERSION 20180730
WORKDIR /
RUN set -eux; \
    yum update -y && yum install -y \
        ca-certificates \
        gcc \
        gcc-c++ \
        make \
        cmake \
        git \
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

FROM centos:latest
RUN set -eux \
    yum update -y && yum install -y ca-certificates
COPY --from=build /boringssl .
WORKDIR /boringssl