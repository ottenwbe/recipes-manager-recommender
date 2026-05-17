FROM docker.io/python:3.14-alpine
LABEL maintainer="ottenwbe.public@gmail.com"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_APP="analyzer"

# Create a non-root user for security
RUN adduser -D recommender
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=recommender:recommender analyzer/ ./analyzer/

USER recommender

EXPOSE 5000

ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "1", "--threads", "4", "analyzer:app"]