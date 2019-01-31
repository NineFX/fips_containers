FROM alpine:latest

RUN apk add --no-cache \
		ca-certificates

RUN [ ! -e /etc/nsswitch.conf ] && echo 'hosts: files dns' > /etc/nsswitch.conf

ENV GOLANG_BORINGCRYPTO_VERSION 1.11

RUN set -eux; \
	apk add --no-cache --virtual .build-deps \
		bash \
		tar \
		git \
		gcc \
		musl-dev \
		openssl \
		go \
	; \
	export \
		GOROOT_BOOTSTRAP="$(go env GOROOT)" \
		GOOS="$(go env GOOS)" \
		GOARCH="$(go env GOARCH)" \
		GOHOSTOS="$(go env GOHOSTOS)" \
		GOHOSTARCH="$(go env GOHOSTARCH)" \
	; \
	apkArch="$(apk --print-arch)"; \
	case "$apkArch" in \
		armhf) export GOARM='6' ;; \
		x86) export GO386='387' ;; \
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
	apk del .build-deps; \
	\
	export PATH="/usr/local/go/bin:$PATH"; \
	go version

ENV GOPATH /go
ENV PATH $GOPATH/bin:/usr/local/go/bin:$PATH

RUN mkdir -p "$GOPATH/src" "$GOPATH/bin" && chmod -R 777 "$GOPATH"
WORKDIR $GOPATH