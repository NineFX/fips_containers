FROM ubuntu:18.04 AS build

RUN set -eux; \
    apt-get -y update; \
    apt-get -y install \
        ca-certificates \
        software-properties-common \
        wget \
        gnupg2 \
        ninja-build; \
    wget -O - https://apt.llvm.org/llvm-snapshot.gpg.key; \
    apt-key add llvm-snapshot.gpg.key; \
    apt-add-repository "deb http://apt.llvm.org/bionic/ llvm-toolchain-bionic-6.0 main"; \
    apt-get -y update && apt-get -y install clang-6.0; \
    apt-add-repository ppa:gophers/archive; \
    apt-get -y install golang-1.10
