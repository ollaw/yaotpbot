FROM python:3.10-slim AS builder

WORKDIR /app

RUN apt update && apt install -y curl git && \
    curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:${PATH}"

COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false && poetry install --without dev --no-root

COPY . .

RUN poetry build

FROM python:3.10-slim AS runner
WORKDIR /app

COPY --from=builder /app/dist/*.whl /app/
RUN pip3 install /app/*.whl

RUN adduser --system --no-create-home yaoptuser
USER yaoptuser

CMD ["run-bot"]
