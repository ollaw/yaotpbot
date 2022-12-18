FROM python:3.8-slim as builder
WORKDIR /app
COPY . .
RUN pip3 install --upgrade build
RUN apt update && apt install git -y
RUN python3 -m build

FROM python:3.8-slim as runner
WORKDIR /app
RUN apt update && apt install -y cargo gcc libffi-dev libssl-dev && rm -rf /var/lib/apt/lists/*
RUN pip3 install cryptography==3.3.2
RUN pip3 install --upgrade yaotpbot
RUN adduser --system --no-create-home yaoptuser

USER yaoptuser

CMD run-bot
