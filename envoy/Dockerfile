FROM ninefx/boringcrypto:20181025-ubuntu AS build_stage_1

FROM envoyproxy/envoy-build-ubuntu:4b0b6540a1c34423813c6a81967cd6656c7b8f05 AS build_stage_2
COPY --from=build_stage_1 /boringssl /boringssl


## KEY DIRECTIVES FOR THE FUTURE OF THE PROJECT:
# What needs to eventually happen if this fleet
# of containers ever is unshelved in the future is
# to somehow get envoy to build on top of our 
# BoringCrypto container. This is going to require
# cloning the EnvoyProxy master branch and figuring
# out a way to (1) switch on FIPS mode in the Bazel
# builder and (2) ensure that the Bazel builder
# points to the BoringCrypto module built using our
# Docker environment (as this is guaranteed
# FIPS-validated and the way Envoy pulls
# BoringCrypto as-is is NOT). This is a massive task
# within itself as it would require extensive
# knowledge of the Bazel build system and sub-
# stantial rewiring of the Envoy codebase to fit our
# needs.
