# syntax=docker/dockerfile:1
FROM python:3.11-slim as base

ENV PYTHONDONTWRITEBYTECODE=1     PYTHONUNBUFFERED=1

WORKDIR /app

# Install runtime deps
COPY app/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Add non-root user
RUN useradd -m appuser
USER appuser

# Copy app code
COPY app/ /app/

EXPOSE 80

# Healthcheck (optional)
# Note: curl is not installed by default in slim, so we use python to check.
HEALTHCHECK CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1/health').read()" || exit 1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
