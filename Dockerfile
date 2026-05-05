# syntax=docker/dockerfile:1
FROM cgr.dev/chainguard/python:latest-dev AS builder

WORKDIR /app

COPY requirements.txt ./
RUN python -m venv /app/venv
ENV PATH="/app/venv/bin:$PATH"
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app

FROM cgr.dev/chainguard/python:latest

WORKDIR /app

COPY --from=builder /app/venv /app/venv
COPY app ./app

ENV PATH="/app/venv/bin:$PATH"

ENTRYPOINT ["/app/venv/bin/python"]
CMD ["-m", "app"]