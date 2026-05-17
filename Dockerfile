FROM docker.io/python:3.14-alpine
LABEL maintainer="ottenwbe.public@gmail.com"

# Create a non-root user for security
RUN adduser -D recommender

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY analyzer/ ./analyzer/

EXPOSE 5000

USER recommender

ENV FLASK_APP="analyzer"

# Use Gunicorn for production
ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:5000", "analyzer:app"]