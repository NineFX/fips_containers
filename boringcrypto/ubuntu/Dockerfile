FROM ubuntu:18.04 AS build

RUN set -eux; \
    apt-get -y update; \
    apt-get -y install \
        ca-certificates \
        software-properties-common \
        wget \
        gnupg2 \
        tar \
        ninja-build=1.8.2\*; \
    wget -O - https://apt.llvm.org/llvm-snapshot.gpg.key | apt-key add -; \
    apt-get -y update; \
    apt-add-repository "deb http://apt.llvm.org/bionic/ llvm-toolchain-bionic-6.0 main"; \
    apt-get -y install clang-6.0 lld-6.0; \
    wget -O - https://dl.google.com/go/go1.10.3.linux-amd64.tar.gz; \
    tar -C /usr/local -xzf go1.10.3.linux-amd64.tar.gz; \
    export PATH=$PATH:/usr/local/go/bin