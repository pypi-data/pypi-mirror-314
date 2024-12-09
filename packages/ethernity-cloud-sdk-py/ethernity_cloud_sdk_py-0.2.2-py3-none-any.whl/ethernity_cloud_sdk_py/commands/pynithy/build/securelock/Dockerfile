FROM etny-securelock-serverless AS release

COPY ./src/serverless/requirements.txt /requirements.txt
RUN pip3 install -r /requirements.txt
RUN rm -rf /requirements.txt

ENV SECURELOCK_SESSION=ec_sdk_py_win_06_SECURELOCK_V3_testnet_92
ENV BUCKET_NAME=etny-pynithy-testnet-v3
ENV SMART_CONTRACT_ADDRESS=0x02882F03097fE8cD31afbdFbB5D72a498B41112c
ENV IMAGE_REGISTRY_ADDRESS=0x15D73a742529C3fb11f3FA32EF7f0CC3870ACA31
ENV RPC_URL=https://core.bloxberg.org
ENV CHAIN_ID=8995
ENV TRUSTED_ZONE_IMAGE=etny-pynithy-testnet

RUN mkdir binary-fs-dir

COPY ./src /etny-securelock/
COPY ./scripts/* /etny-securelock/

RUN /etny-securelock/binary-fs-build.sh

FROM registry.ethernity.cloud:443/debuggingdelight/ethernity-cloud-sdk-registry/sconecuratedimages/crosscompilers AS build

COPY --from=release /binary-fs-dir /.

RUN scone gcc ./binary_fs_blob.s ./libbinary_fs_template.a -shared -o /libbinary-fs.so

FROM etny-securelock-serverless

COPY --from=build /usr/local/bin/scone /usr/local/bin/scone

#RUN scone cas attest scone-cas.cf 3061b9feb7fa67f3815336a085f629a13f04b0a1667c93b14ff35581dc8271e4 -GCS --only_for_testing-debug --only_for_testing-ignore-signer

COPY --from=build /libbinary-fs.so /lib/libbinary-fs.so

RUN openssl genrsa -3 -out /enclave-key.pem 3072


ENV SCONE_HEAP=3072M
ENV SCONE_LOG=FATAL
ENV SCONE_STACK=4M
ENV SCONE_ALLOW_DLOPEN=1
ENV SCONE_EXTENSIONS_PATH=/lib/libbinary-fs.so

# Disabled production mode for testnet
# RUN scone-signer sign --key=/enclave-key.pem --env --production /usr/local/bin/python3

RUN rm -rf /enclave-key.pem


ENTRYPOINT ["/usr/local/bin/python", "/etny-securelock/securelock.py"]
