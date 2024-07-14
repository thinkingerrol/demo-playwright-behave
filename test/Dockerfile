FROM mcr.microsoft.com/playwright/python:v1.36.0-jammy-amd64

RUN pip install --no-cache-dir playwright==1.41.1 behave==1.2.6
RUN playwright install chromium

RUN mkdir -p /test/build
COPY . /test/
WORKDIR /test

# NOTE: for some reason the "set -e; trap '' EXIT" avoids hanging
CMD ["bash", "-c", "set -e; trap '' EXIT; xvfb-run behave --tags ~@skip --no-skipped"]
