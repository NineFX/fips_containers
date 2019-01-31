FROM centos:latest

ENV GOLANG_BORINGCRYPTO_VERSION 1.11

RUN set -eux; \
    yum update; \
    yum install -y \
		curl \
        ca-certificates \
		gcc \
        gcc-c++ \
        glibc-devel \
        git \
        make \
    ; \
	rpm --import https://mirror.go-repo.io/centos/RPM-GPG-KEY-GO-REPO; \
	curl -s https://mirror.go-repo.io/centos/go-repo.repo | tee /etc/yum.repos.d/go-repo.repo; \
	yum install -y golang; \
	\
	export \
		GOROOT_BOOTSTRAP="$(go env GOROOT)" \
		GOOS="$(go env GOOS)" \
		GOARCH="$(go env GOARCH)" \
		GOHOSTOS="$(go env GOHOSTOS)" \
		GOHOSTARCH="$(go env GOHOSTARCH)" \
	; \
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
	rpm -e --nodeps \
		curl \
		ca-certificates \
		gcc \
		gcc-c++ \
		glibc-devel \
		git \
		make \
		golang \
		golang-src-1.11.4-0.el7.noarch; \
	rm -f /etc/yum.repos.d/go-repo.repo; \
	export PATH="/usr/local/go/bin:$PATH"; \
	go version

ENV GOPATH /go
ENV PATH $GOPATH/bin:/usr/local/go/bin:$PATH

RUN mkdir -p "$GOPATH/src" "$GOPATH/bin" && chmod -R 777 "$GOPATH"
WORKDIR $GOPATH