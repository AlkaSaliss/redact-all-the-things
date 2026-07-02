FROM python:3.12-slim

WORKDIR /app
COPY worker_stub.py /app/worker_stub.py

USER nobody
ENTRYPOINT ["python", "/app/worker_stub.py"]
