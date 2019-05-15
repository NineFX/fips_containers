FROM ninefx/boringcrypto:20181025-ubuntu AS build_stage_1

FROM envoyproxy/envoy-build-ubuntu:4b0b6540a1c34423813c6a81967cd6656c7b8f05 AS build_stage_2
COPY --from=build_stage_1 /boringssl /boringssl