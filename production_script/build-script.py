import yaml
from os import popen, chdir, system

# READ IN YAML FILE
with open('packages.yml', 'r') as yamlstream:
    try:
        raw = yaml.load(yamlstream)
    except yaml.YAMLError as e:
        print e

# SHASUM VALIDATION FUNCTION
def valid_shasum(url, sha256):
    actual_sha256 = popen('curl -s ' + url + ' | shasum -a 256') \
            .read() \
            .split()[0]
    print(sha256)
    print(actual_sha256)
    return actual_sha256 == sha256


def gen_df_deps(package_url, package_name):
    return '''FROM ish512/fips-go:1.0-alpine AS build
WORKDIR /
RUN set -eux; \\
    apk add --no-cache \\
    ca-certificates \\
    curl \\
    gcc \\
    g++ \\
    make \\
    cmake \\
    perl \\
    tar; \\
curl -O {url}; \\
tar -zxvf {name}.tar.gz; \\
cd {name}; \\ '''.format(url=package_url, name=package_name)


def gen_df_stage2(package_name):
    return '''
        
FROM alpine:latest
RUN set -eux; \\
    apk add --no-cache ca-certificates
COPY --from=build /{name} .
WORKDIR /{name}'''.format(name=package_name)

# MASTER FOR-LOOP
for package in raw:
    # SHASUM VERIFICATION STEP - PROGRAM EXITS IF A SHASUM CHECK FAILS
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
    # ALPINE DOCKERFILE GENERATION STEP
    popen('mkdir ' + name)
    chdir(name)
    with open('Dockerfile', 'w') as dfstream:
        dfstream.write(gen_df_deps(url, name))
        if (name == 'openssl-fips-2.0.16'):
            dfstream.write('''
        ./config; \\
        make; \\
        make install''')
        else if (name == 'boringssl-24e5886c0edfc409c8083d10f9f1120111efd6f5'):
            dfstream.write('''
        
        ''')
        dfstream.write(gen_df_stage2(name))
    #system('docker build -t \"' + name + '\" .')
    chdir('..')
