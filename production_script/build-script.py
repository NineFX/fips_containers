import yaml
from os import popen, chdir, system

# YAML file read-in
with open('packages.yml', 'r') as yamlstream:
    try:
        raw = yaml.load(yamlstream)
    except yaml.YAMLError as e:
        print e


# Validates the sha256 sum of a package.
# Returns true if the expected sha256 matches the actual sha256
def valid_shasum(url, sha256):
    actual_sha256 = popen('curl -s ' + url + ' | shasum -a 256') \
            .read() \
            .split()[0]
    print('Expected shasum: ' + sha256)
    print('Actual shasum: ' + actual_sha256)
    return actual_sha256 == sha256


# Generates the Dockerfile script for the dependencies of all packages
def df_gen_deps():
    return '''FROM ish512/fips-go:1.0-alpine AS build
WORKDIR /
RUN set -eux; \\
    apk add --no-cache \\
        ca-certificates \\
        linux-headers \\
        curl \\
        gcc \\
        g++ \\
        make \\
        cmake \\
        perl \\
        tar \\
        xz; \\'''


# Generates the Dockerfile script for the build step of each package
def df_build_step(package_url, package_name):
    return {
        'openssl-fips-2.0.16': '''
    curl -O {url}; \\
    tar -zxvf {name}.tar.gz; \\
    cd {name}; \\
    ./config; \\
    make; \\
    make install'''.format(url=package_url, name=package_name),
        'boringssl-24e5886c0edfc409c8083d10f9f1120111efd6f5': '''
    curl -O {url}; \\
    tar -xvf {name}.tar.xz; \\
    mv boringssl {name}; \\
    cd {name}; \\
    mkdir build; \\
    cd build; \\
    cmake ..; \\
    make; \\
    cd ..; \\
    go run util/all_tests.go'''.format(url=package_url, name=package_name)
    }.get(package_name, 'Invalid package!')


# Generates the Dockerfile script necessary for a successful multi-stage build
def df_gen_stage2(package_name):
    return '''

FROM alpine:latest
RUN set -eux; \\
    apk add --no-cache ca-certificates
COPY --from=build /{name} .
WORKDIR /{name}'''.format(name=package_name)


# Main program loop
for package in raw:
    # Sha256 verification step - program exits if any sha256 sum check fails
    pkg = package.keys()[0]
    url = package[package.keys()[0]]['url']
    sha256 = package[package.keys()[0]]['sha256']
    version = package[package.keys()[0]]['version']
    name = pkg + '-' + version
    if(not valid_shasum(url, sha256)):
        print('sha256 sum check failed for package ' + name + ', exiting...')
        break
    else:
        print('shasum verification step passed for ' + name)
    # Alpine dockerfile generation step
    popen('mkdir ' + name)
    chdir(name)
    with open('Dockerfile', 'w') as dfstream:
        dfstream.write(df_gen_deps())
        dfstream.write(df_build_step(url, name))
        dfstream.write(df_gen_stage2(name))
    # Alpine dockerfile build step
    system('docker build -t \"' + name + '\" .')
    chdir('..')
