FROM ninefx/fips-go:1.0-ubuntu AS build

ENV BAZEL_VERSION=0.24.0

RUN set -eux; \
    # Bazel install
    apt-get -y update && apt-get -y install ca-certificates openjdk-8-jdk wget gnupg2; \
    echo "deb [arch=amd64] http://storage.googleapis.com/bazel-apt stable jdk1.8" | tee /etc/apt/sources.list.d/bazel.list; \
    wget https://bazel.build/bazel-release.pub.gpg; \
    apt-key add bazel-release.pub.gpg; \
    apt-get -y update && apt-get -y install bazel; \
    apt-get -y install --only-upgrade bazel; \
    # EnvoyProxy dependencies
    apt-get -y install \
        libtool \
        cmake \
        clang-format-7 \
        automake \
        autoconf \
        make \
        ninja-build \
        curl \
        virtualenv; \
    # Building EnvoyProxy
    go get -u github.com/bazelbuild/buildtools/buildifier; \
    export BUILDIFIER_BIN="$GOPATH/bin/buildifier"; \
    touch WORKSPACE; \
    bazel build //source/exe:envoy-static; \
    envoy --version | grep "BoringSSL-FIPS"