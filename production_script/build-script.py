import yaml
from os import popen

# READ IN YAML FILE
with open('fips-packages.yml', 'r') as yamlstream:
    try:
        raw = yaml.load(yamlstream)
    except yaml.YAMLError as e:
        print e

# FUNCTION FOR SHASUM CHECKS
verify = lambda url, sha256: popen('curl -s ' + url + ' | shasum -a 256').read().split()[0] != sha256

# MASTER FOR-LOOP
for package in raw:
    # SHASUM VERIFICATION STEP - PROGRAM EXITS IF A SHASUM CHECK FAILS
    url = package[package.keys()[0]]['url']
    sha256 = package[package.keys()[0]]['sha256']
    if(verify(url, sha256)):
        print 'sha256 sum check failed for package ' + package.keys()[0] + ', exiting...'
        break
    # ALPINE DOCKERFILE GENERATION STEP
    with open(package.keys()[0] + '-fips-alpine.Dockerfile', 'w') as fstream:
      fstream.write('FROM alpine:latest')
