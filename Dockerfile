FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    QUIZ_DB_PATH=/data/quiz.db

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
COPY seed.py ./seed.py

# DB lives on a mounted volume so it survives restarts and gets backed up.
RUN mkdir -p /data
VOLUME ["/data"]

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request,sys; sys.exit(0 if urllib.request.urlopen('http://localhost:8080/healthz').status==200 else 1)"

# Seed runs idempotently on every boot, then starts the server.
# IMPORTANT: exactly ONE uvicorn worker (no --workers). The in-process background
# job worker in app/jobs.py runs a single daemon thread per process; multiple
# workers would each start one and double-run/duplicate LLM proposals.
CMD ["sh", "-c", "python -m seed && uvicorn app.main:app --host 0.0.0.0 --port 8080"]
