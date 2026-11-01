#!/usr/bin/env bash
# This script is used only for testing purposes
# Accepts TAG parameter to allow custom image tags (e.g., development-20261101-1430)

MAINTAINER="Beate Ottenwaelder <ottenwbe.public@gmail.com>"
APP_VERSION="development"
DATE=$(date +"%F %T")

# Use custom tag if provided, otherwise default to "development"
TAG=${TAG:-development}

echo "Building recommender image with tag: $TAG"

docker build --label "version=${APP_VERSION}" --label "build_date=${DATE}" --label "maintaner=${MAINTAINER}" \
  -t "docker.io/ottenwbe/recipes-manager-recommender:$TAG" \
  -f Dockerfile .

echo "Successfully built docker.io/ottenwbe/recipes-manager-recommender:$TAG"
