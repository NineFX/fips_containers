import yaml
from os import popen, chdir

# READ IN YAML FILE
with open('packages.yml', 'r') as yamlstream:
    try:
        raw = yaml.load(yamlstream)
    except yaml.YAMLError as e:
        print e

# FUNCTION FOR SHASUM CHECKS
verify = lambda url, sha256: popen('curl -s ' + url + ' | shasum -a 256').read().split()[0] != sha256

# MASTER FOR-LOOP
for package in raw:
    # SHASUM VERIFICATION STEP - PROGRAM EXITS IF A SHASUM CHECK FAILS
    name = package.keys()[0]
    url = package[package.keys()[0]]['url']
    sha256 = package[package.keys()[0]]['sha256']
    version = package[package.keys()[0]]['version']
    if(verify(url, sha256)):
        print 'sha256 sum check failed for package ' + name + ', exiting...'
        break
    # ALPINE DOCKERFILE GENERATION STEP
    pkg_name = name + '-fips-alpine'
    popen('mkdir ' + pkg_name)
    chdir(pkg_name)
    with open('Dockerfile', 'w') as dfstream:
        dfstream.write    ('FROM alpine:latest AS build\n')
        dfstream.write    ('WORKDIR /\n')
        dfstream.write    ('RUN set -eux; \\\n')
        dfstream.write    ('    apk add --no-cache \\\n')
        dfstream.write    ('        ca-certificates \\\n')
        dfstream.write    ('        curl \\\n')
        dfstream.write    ('        gcc \\\n')
        dfstream.write    ('        g++ \\\n')
        dfstream.write    ('        make \\\n')
        dfstream.write    ('        cmake \\\n')
        dfstream.write    ('        git \\\n')
        dfstream.write    ('        perl \\\n')
        dfstream.write    ('        tar; \\\n')
        dfstream.write    ('    curl -O ' + url + '; \\\n')
        dfstream.write    ('    tar -zxvf ' + name + '-' + version + '.tar.gz; \\\n')
        dfstream.write    ('    cd ' + name + '-' + version + '; \\\n')
        if (name == 'openssl'):
            dfstream.write('    ./config; \\\n')
            dfstream.write('    make; \\\n')
            dfstream.write('    make install')
