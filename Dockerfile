FROM python:3.14-slim@sha256:9006fc63e3eaedc00ebc81193c99528575a2f9b9e3fb36d95e94814c23f31f47

WORKDIR /repo

COPY src/package_assets.py /usr/local/bin/package_assets.py

ENTRYPOINT ["python", "/usr/local/bin/package_assets.py"]
