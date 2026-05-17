#!/usr/bin/env bash
# This script is used only for testing purposes

MAINTAINER="Beate Ottenwaelder <ottenwbe.public@gmail.com>"
APP_VERSION="development"
DATE=$(date +"%F %T")
DOCKER_REGISTRY=${DOCKER_REGISTRY:-localhost:5000}

podman build --label "version=${APP_VERSION}" --label "build_date=${DATE}"  --label "maintaner=${MAINTAINER}" -t "${DOCKER_REGISTRY}/ottenwbe/recipes-manager-recommender:development" -f Dockerfile . 
podman push "${DOCKER_REGISTRY}/ottenwbe/recipes-manager-recommender:development" --tls-verify=false
