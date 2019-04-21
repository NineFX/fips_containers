###############################################################################
###############################################################################
# This Docker build for BoringSSL is FIPS 140-2 validated by the
# BoringCrypto FIPS 140-2 Security Policy published by Google on 2018/10/25,
# which can be found at http://bit.ly/2IzFc0V.
# The package dependencies and build instructions reflect those found on p. 19
# of the Security Policy.
###############################################################################
# Copyright 2019 NineFX, Inc.
###############################################################################

FROM ubuntu:16.04 AS build

ENV CLANG clang+llvm-6.0.1-x86_64-linux-gnu-ubuntu-16.04
ENV GO go1.10.3.linux-amd64
ENV BORINGSSL boringssl-66005f41fbc3529ffe8d007708756720529da20d
ENV BORINGSSL_SHA256 b12ad676ee533824f698741bd127f6fbc82c46344398a6d78d25e62c6c418c73

RUN set -eux; \
    apt-get -y update; \
    ## Pre-dependencies/boilerplate packages
    apt-get -y install \
        ca-certificates \
        build-essential \
        wget \
        xz-utils \
        cmake \
        unzip; \
    ## Dependency: Clang 6.0.1
    wget \
        http://releases.llvm.org/6.0.1/${CLANG}.tar.xz; \
    tar -C /usr/local -xJf ${CLANG}.tar.xz; \
    echo "export PATH=/usr/local/${CLANG}/bin/:\$PATH" >> /etc/profile; \
    ln -s /usr/local/${CLANG}/bin/clang /usr/bin/clang; \
    ln -s /usr/local/${CLANG}/bin/clang++ /usr/bin/clang++; \
    if [ ! "clang --version | grep '6.0.1'" ]; \
        then \
        echo 'Fatal: correct clang version not found!' \
        exit 1; \
    fi; \
    ## Dependency: Go 1.10.3
    wget -q https://dl.google.com/go/${GO}.tar.gz; \
    tar -C /usr/local -xzf ${GO}.tar.gz; \
    echo "export PATH=\$PATH:/usr/local/go/bin" >> /etc/profile; \
    ln -s /usr/local/go/bin/go /usr/bin/go; \
    ln -s /usr/local/go/bin/godoc /usr/bin/godoc; \
    ln -s /usr/local/go/bin/gofmt /usr/bin/gofmt; \
    if [ ! "go version | grep '1.10.3'" ]; \
        then \
        echo 'Fatal: correct go version not found!' \
        exit 1; \
    fi; \
    ## Dependency: Ninja 1.8.2
    wget \
        https://github.com/ninja-build/ninja/releases/download/v1.8.2/ninja-linux.zip; \
    unzip ninja-linux.zip -d /usr/bin; \
    if [ "ninja --version" -ne '1.8.2' ]; \
        then \
        echo 'Fatal: correct ninja version not found!' \
        exit 1; \
    fi; \
    ## Create CMake toolchain
    printf \
        "set(CMAKE_C_COMPILER \"clang\")\nset(CMAKE_CXX_COMPILER \"clang++\")\n" \
        >${HOME}/toolchain; \
    ## Verify BoringSSL
    wget \
        https://commondatastorage.googleapis.com/chromium-boringssl-docs/fips/${BORINGSSL}.tar.xz; \
    if [ "sha256sum ${BORINGSSL}.tar.xz" -ne ${BORINGSSL_SHA256}} ]; \
        then \
        echo 'Fatal: invalid sha256sum for ${BORINGSSL}!'; \
        exit 1; \
    fi; \
    ## Build BoringSSL
    tar -xJf ${BORINGSSL}.tar.xz; \
    cd boringssl; \
    mkdir build; \
    cd build; \
    cmake \
        -GNinja \
        -DCMAKE_TOOLCHAIN_FILE=${HOME}/toolchain \
        -DFIPS=1 \
        -DCMAKE_BUILD_TYPE=Release ..; \
    ninja; \
    ninja run_tests


FROM ubuntu:18.04

COPY --from=build /boringssl /boringssl

RUN ./boringssl/build/tool/bssl isfips