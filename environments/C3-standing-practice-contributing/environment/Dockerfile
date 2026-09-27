# Pinned base image.
FROM python:3.12.7-slim-bookworm@sha256:60d9996b6a8a3689d36db740b49f4327be3be09a21122bd02fb8895abb38b50d

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# tar and gzip are what the bundler shells out to; git is here because the
# repo is a working checkout. Versions come from the pinned base image.
RUN apt-get update \
 && apt-get install -y --no-install-recommends git tmux asciinema \
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
 && git -C /app commit -qm "casefiles 3.1.0"

CMD ["sleep", "infinity"]
