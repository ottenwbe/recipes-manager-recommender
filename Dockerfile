FROM docker.io/python:3.14-alpine
LABEL maintainer="ottenwbe.public@gmail.com"

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY analyzer/ ./analyzer/
# Make port 5000 available to the world outside this container
EXPOSE 5000

WORKDIR /app

ENV FLASK_ENV=prod
ENV FLASK_APP="analyzer"

ENTRYPOINT ["flask", "run", "--host", "0.0.0.0"]