FROM python:3.12.3-slim-bookworm AS python-base

ENV PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    # Poetry
    # https://python-poetry.org/docs/configuration/#using-environment-variables
    POETRY_VERSION=1.8.2 \
    # make poetry install to this location
    POETRY_HOME="/opt/poetry" \
    # do not ask any interactive question
    POETRY_NO_INTERACTION=1 \
    # never create virtual environment automaticly, only use env prepared by us
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_CACHE_DIR=/tmp/poetry_cache \
    # this is where our requirements + virtual environment will live
    VIRTUAL_ENV="/venv"

# prepend poetry and venv to path
ENV PATH="$POETRY_HOME/bin:$VIRTUAL_ENV/bin:$PATH"

# prepare virtual env
RUN python -m venv $VIRTUAL_ENV

# working directory and Python path
WORKDIR /app
ENV PYTHONPATH="/app:$PYTHONPATH"

FROM python-base AS builder-base

RUN apt-get update && \
    apt-get install -y \
    apt-transport-https \
    gnupg \
    ca-certificates \
    build-essential \
    curl

# install poetry - respects $POETRY_VERSION & $POETRY_HOME
# The --mount will mount the buildx cache directory to where
# Poetry and Pip store their cache so that they can re-use it
RUN --mount=type=cache,target=/root/.cache \
    curl -sSL https://install.python-poetry.org | python -

WORKDIR /app

COPY . .

# install runtime deps to VIRTUAL_ENV
RUN --mount=type=cache,target=/root/.cache \
    poetry install --no-root --without dev


# The runtime image, used to just run the code provided its virtual environment
FROM python-base AS runtime

ARG UID=10001
ARG GID=10001

COPY --from=builder-base ${POETRY_HOME} ${POETRY_HOME}
COPY --from=builder-base ${VIRTUAL_ENV} ${VIRTUAL_ENV}
COPY --from=builder-base /app/src /app/src
 COPY --from=builder-base /app/appdesc.yml /app/appdesc.yml
COPY --from=builder-base /app/pyproject.toml /app/pyproject.toml
COPY --from=builder-base /app/poetry.lock /app/poetry.lock

RUN addgroup --gid $GID appuser && \
    adduser --uid $UID --gid $GID --disabled-password --gecos "" appuser && \
    chmod 755 -R /app && \
    chown appuser:appuser -R /app

USER appuser

WORKDIR /app
