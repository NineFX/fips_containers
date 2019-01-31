FROM ubuntu:latest

ENV GOLANG_BORINGCRYPTO_VERSION 1.11

RUN set -eux; \
    apt-get update; \
    apt-get install -y --no-install-recommends \
        ca-certificates \
		g++ \
        gcc \
        golang-go \
        libc6-dev \
        git-core \
        make \
        pkg-config \
    && rm -rf /var/lib/apt/lists/* \
    ; \
	export \
		GOROOT_BOOTSTRAP="$(go env GOROOT)" \
		GOOS="$(go env GOOS)" \
		GOARCH="$(go env GOARCH)" \
		GOHOSTOS="$(go env GOHOSTOS)" \
		GOHOSTARCH="$(go env GOHOSTARCH)" \
	; \
	dpkgArch="$(dpkg --print-architecture)"; \
	case "$dpkgArch" in \
		armhf) export GOARM='6' ;; \
		amd64) export GO386='387' ;; \
	esac; \
	\
	git clone --single-branch --branch dev.boringcrypto.go${GOLANG_BORINGCRYPTO_VERSION} https://github.com/golang/go.git; \
	tar -czf go.tgz go; \
	rm -rf go; \
	tar -C /usr/local -xzf go.tgz; \
	rm go.tgz; \
	\
	cd /usr/local/go/src; \
	./make.bash; \
	\
	rm -rf \
		/usr/local/go/pkg/bootstrap \
		/usr/local/go/pkg/obj \
	; \
	apt-get autoremove --purge -y g++ gcc golang-go libc6-dev git-core make pkg-config; \
	\
	export PATH="/usr/local/go/bin:$PATH"; \
	go version

ENV GOPATH /go
ENV PATH $GOPATH/bin:/usr/local/go/bin:$PATH

RUN mkdir -p "$GOPATH/src" "$GOPATH/bin" && chmod -R 777 "$GOPATH"
WORKDIR $GOPATH