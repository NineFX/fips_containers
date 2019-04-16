FROM ubuntu:16.04 AS build

ENV CLANG clang+llvm-6.0.1-x86_64-linux-gnu-ubuntu-16.04
ENV GO go1.10.3.linux-amd64

RUN set -eux; \
    apt-get -y update; \
    # Build dependencies
    apt-get -y install \
        ca-certificates \
        wget \
        xz-utils \
        cmake; \
    ## BoringCrypto dependency 1: Clang 6.0.1
    wget http://releases.llvm.org/6.0.1/${CLANG}.tar.xz; \
    tar -xJf ${CLANG}.tar.xz; \
    mv ${CLANG}/ /usr/local; \
    echo "export PATH=/usr/local/${CLANG}/bin/:\$PATH" >> /etc/profile; \
    ln -s /usr/local/${CLANG}/bin/clang /usr/bin/clang; \
    ln -s /usr/local/${CLANG}/bin/clang++ /usr/bin/clang++; \
    clang --version; \
    cd /; \
    ## BoringCrypto dependency 2: Go 1.10.3
    wget https://dl.google.com/go/${GO}.tar.gz; \
    tar -C /usr/local -xzf ${GO}.tar.gz; \
    echo "export PATH=\$PATH:/usr/local/go/bin" >> /etc/profile; \
    go --version
