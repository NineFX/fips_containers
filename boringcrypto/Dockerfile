#################################################################################################################################
# This Docker build for BoringSSL is FIPS 140-2 validated by the BoringCrypto FIPS 140-2 Security Policy published by Google on
# 2018/10/25, which can be found at
# https://csrc.nist.gov/CSRC/media/projects/cryptographic-module-validation-program/documents/security-policies/140sp3318.pdf
#
# The package dependencies and build instructions reflect those found on p. 19 of the Security Policy.
#################################################################################################################################
# Copyright 2019 NineFX, Inc.
#################################################################################################################################

### BUILD IMAGE
FROM ubuntu:16.04 AS build

ENV CLANG clang+llvm-6.0.1-x86_64-linux-gnu-ubuntu-16.04
ENV GO go1.10.3.linux-amd64
ENV BORINGSSL boringssl-66005f41fbc3529ffe8d007708756720529da20d
ENV BORINGSSL_SHA256 b12ad676ee533824f698741bd127f6fbc82c46344398a6d78d25e62c6c418c73

SHELL ["/bin/bash", "-o", "pipefail", "-c"]
RUN set -eux; \
    apt-get -y update; \
    ## Pre-dependencies/boilerplate packages
    apt-get -y install --no-install-recommends \
        ca-certificates=20170717~16.04.2 \
        build-essential=12.1ubuntu2 \
        wget=1.17.1-1ubuntu1.5 \
        xz-utils=5.1.1alpha+20120614-2ubuntu2 \
        cmake=3.5.1-1ubuntu3 \
        unzip=6.0-20ubuntu1; \
    ## Dependency: Clang 6.0.1
    wget "http://releases.llvm.org/6.0.1/${CLANG}.tar.xz"; \
    tar -C /usr/local -xJf ${CLANG}.tar.xz; \
    echo "export PATH=/usr/local/${CLANG}/bin/:\$PATH" >> /etc/profile; \
    ln -s /usr/local/${CLANG}/bin/clang /usr/bin/clang; \
    ln -s /usr/local/${CLANG}/bin/clang++ /usr/bin/clang++; \
    ## Dependency: Go 1.10.3
    wget "https://dl.google.com/go/${GO}.tar.gz"; \
    tar -C /usr/local -xzf ${GO}.tar.gz; \
    echo "export PATH=\$PATH:/usr/local/go/bin" >> /etc/profile; \
    ln -s /usr/local/go/bin/go /usr/bin/go; \
    ln -s /usr/local/go/bin/godoc /usr/bin/godoc; \
    ln -s /usr/local/go/bin/gofmt /usr/bin/gofmt; \
    ## Dependency: Ninja 1.8.2
    wget "https://github.com/ninja-build/ninja/releases/download/v1.8.2/ninja-linux.zip"; \
    unzip ninja-linux.zip -d /usr/bin; \
    ## Create CMake toolchain
    printf "set(CMAKE_C_COMPILER \"clang\")\nset(CMAKE_CXX_COMPILER \"clang++\")\n" > /toolchain; \
    ## Verify BoringSSL
    wget "https://commondatastorage.googleapis.com/chromium-boringssl-docs/fips/${BORINGSSL}.tar.xz"; \
    sha256="$(sha256sum ${BORINGSSL}.tar.xz | cut -d' ' -f1)"; \
    if [ "$sha256" != "${BORINGSSL_SHA256}" ]; \
        then \
        echo "Fatal: invalid sha256sum for ${BORINGSSL}!"; \
        exit 1; \
    fi; \
    ## Build BoringSSL
    tar -xJf ${BORINGSSL}.tar.xz; \
    mkdir -p boringssl/build
WORKDIR /boringssl/build
RUN cmake \
        -GNinja \
        -DCMAKE_TOOLCHAIN_FILE=/toolchain \
        -DFIPS=1 \
        -DCMAKE_BUILD_TYPE=Release \
        ..; \
    ninja; \
    ninja run_tests

### DEPLOYMENT IMAGE
FROM ubuntu:18.04

COPY --from=build /boringssl /boringssl

CMD [ "./boringssl/build/tool/bssl", "isfips" ]
