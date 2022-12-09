FROM --platform=$BUILDPLATFORM python:3.8-slim as builder
WORKDIR /app
RUN pip3 install --upgrade build
COPY pyproject.toml pyproject.toml
ADD otpbot otpbot
RUN python3 -m build

FROM --platform=$BUILDPLATFORM python:3.8-slim as runtime
WORKDIR /app
COPY --from=builder /app/dist/* /app
RUN pip3 install *.whl
RUN adduser --system --no-create-home yaoptuser

USER yaoptuser

CMD run-bot