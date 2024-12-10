FROM python:3.12.0-slim AS base
LABEL org.opencontainers.image.name=europe-west3-docker.pkg.dev/zeitonline-engineering/docker-zon/deploynotify
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --no-deps -r requirements.txt

FROM base AS testing
COPY requirements-testing.txt .
RUN pip install --no-cache-dir --no-deps -r requirements-testing.txt
ENV PYTHONDONTWRITEBYTECODE 1
COPY pyproject.toml *.rst ./
COPY src/zeit/deploynotify/__init__.py src/zeit/deploynotify/
RUN pip install --no-cache-dir --no-deps -e .

FROM base AS production
COPY pyproject.toml *.rst ./
COPY src src
RUN pip install --no-cache-dir -e . && pip check
ENTRYPOINT ["python", "-m", "zeit.deploynotify"]
