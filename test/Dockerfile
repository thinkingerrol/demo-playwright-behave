FROM mcr.microsoft.com/playwright/python:v1.48.0-noble

RUN pip install --no-cache-dir playwright==1.48.0 behave==1.2.6
RUN playwright install chromium

RUN mkdir -p /build /videos
COPY . /

CMD ["bash", "/test/entrypoint.sh"]
