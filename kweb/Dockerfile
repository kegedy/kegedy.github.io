FROM python:3.12-slim

# System libraries the klayout wheel links against that the slim image doesn't ship
# (it bundles the rest); without libexpat1 `import klayout.db` fails at startup.
RUN apt-get update \
    && apt-get install -y --no-install-recommends libexpat1 zlib1g libstdc++6 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Hugging Face Spaces run containers as uid 1000
RUN useradd -m -u 1000 user
USER user
WORKDIR /home/user/app
COPY --chown=user . .

EXPOSE 7860
# --proxy-headers: the Space sits behind an HTTPS proxy; without this kweb builds
# a ws:// websocket URL and browsers block it as mixed content.
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860", "--proxy-headers", "--forwarded-allow-ips=*"]
