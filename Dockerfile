FROM python:3.8-slim as runtime
WORKDIR /app
RUN apt update && apt install -y cargo gcc libffi-dev libssl-dev && rm -rf /var/lib/apt/lists/*
RUN pip3 install yaotpbot
RUN adduser --system --no-create-home yaoptuser

USER yaoptuser

CMD run-bot
