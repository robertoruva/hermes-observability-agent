FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_ROOT_USER_ACTION=ignore
ENV HERMES_CONTAINER_RUNTIME=docker

WORKDIR /app

RUN addgroup --system hermes \
    && adduser --system --ingroup hermes hermes

COPY pyproject.toml README.md LICENSE ./

FROM base AS runtime

COPY src ./src
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir .

USER hermes

EXPOSE 8790

CMD ["uvicorn", "hermes.interfaces.http.app:app", "--host", "0.0.0.0", "--port", "8790"]

FROM base AS test

COPY src ./src
COPY tests ./tests

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir ".[dev]"

USER hermes

CMD ["python", "-m", "unittest", "discover", "-s", "tests"]
