# syntax=docker/dockerfile:1
FROM dhi.io/python:3.14-dev@sha256:b4b5ea6a19c0d92dd737ba2dacb92bc0c2650b771f58864def15ae977716f4ad AS builder

WORKDIR /app

COPY requirements.txt ./
RUN python -m venv /app/venv
ENV PATH="/app/venv/bin:$PATH"
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app

FROM dhi.io/python:3.14@sha256:9566f423e8bfeec5f2acd3bda4e9040a397431e1d8b90210252bc85e4eb2b04a

WORKDIR /app

COPY --from=builder /app/venv /app/venv
COPY app ./app

ENV PATH="/app/venv/bin:$PATH"

ENTRYPOINT ["/app/venv/bin/python"]
CMD ["-m", "app"]