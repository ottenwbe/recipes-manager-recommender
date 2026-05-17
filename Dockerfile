FROM docker.io/python:3.14-alpine
LABEL maintainer="ottenwbe.public@gmail.com"

# Create a non-root user for security
RUN adduser -D recommender

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY analyzer/ ./analyzer/

EXPOSE 5000

# Verify that gunicorn is responding on the expected port
HEALTHCHECK --interval=10s --timeout=3s --start-period=5s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:5000/api/v1/recommendation/health || exit 1

USER recommender

ENV FLASK_APP="analyzer"

# Use Gunicorn for production
ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:5000", "analyzer:app"]