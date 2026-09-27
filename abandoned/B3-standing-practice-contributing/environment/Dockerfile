# Pinned base image.
FROM python:3.12.7-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

RUN apt-get update \
 && apt-get install -y --no-install-recommends git sqlite3 tmux asciinema \
 && rm -rf /var/lib/apt/lists/*

# Baked in so grading needs no network.
RUN pip install --no-cache-dir pytest==8.3.3

WORKDIR /app
COPY repo/ /app/

RUN python /app/scripts/seed_data.py \
 && git init -q /app \
 && git -C /app config user.email dev@example.invalid \
 && git -C /app config user.name dev \
 && git -C /app add -A \
 && git -C /app commit -qm "ledgerq 1.9.3"

CMD ["sleep", "infinity"]
