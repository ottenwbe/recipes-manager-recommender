#!/bin/bash
set -e

IMAGE_NAME="ottenwbe/recipes-manager-recommender:local"
CONTAINER_NAME="smoke-test-local"
PORT=5000 # Ensure this matches the EXPOSE port in your Dockerfile
HEALTH_ENDPOINT="/api/v1/recommendation/health" # Ensure this matches your Flask app's health route

echo "--- Starting Local Smoke Test ---"

# --- Cleanup function to ensure container is stopped and removed ---
cleanup() {
    echo "Cleaning up..."
    if podman ps -a --format "{{.Names}}" | grep -q "$CONTAINER_NAME"; then
        echo "Stopping and removing container '$CONTAINER_NAME'..."
        podman stop "$CONTAINER_NAME" > /dev/null
        podman rm "$CONTAINER_NAME" > /dev/null
    fi
    echo "Cleanup complete."
}
trap cleanup EXIT

echo "1. Building Podman image..."
# Use podman build to align with local minikube scripts and avoid HEALTHCHECK warning
podman build -t "$IMAGE_NAME" -f Dockerfile .

echo "2. Checking if port $PORT is in use..."
# Check if port is already in use
if ss -tuln | grep -q ":$PORT "; then
    echo "Error: Port $PORT is already in use. Please free it before running the smoke test."
    exit 1
fi

echo "3. Starting container..."
# Remove existing container if it exists (cleanup trap will also handle this)
podman rm -f "$CONTAINER_NAME" 2>/dev/null || true

podman run -d -p $PORT:5000 --name "$CONTAINER_NAME" "$IMAGE_NAME"

echo "4. Waiting for application health check (via $HEALTH_ENDPOINT)..."
MAX_RETRIES=30
COUNT=0

while [ $COUNT -lt $MAX_RETRIES ]; do
    HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:$PORT$HEALTH_ENDPOINT || echo "000")
    
    if [ "$HTTP_STATUS" = "200" ]; then
        echo "Success: Application is healthy and Gunicorn is responding on $HEALTH_ENDPOINT!"
        break
    fi
    
    echo "Current HTTP status for $HEALTH_ENDPOINT: $HTTP_STATUS. Waiting... ($((COUNT+1))/$MAX_RETRIES)"
    sleep 1
    COUNT=$((COUNT+1))
done

if [ $COUNT -eq $MAX_RETRIES ]; then
    echo "Failure: Application health check timed out after $MAX_RETRIES seconds."
    echo "Podman logs for '$CONTAINER_NAME':"
    podman logs "$CONTAINER_NAME"
    exit 1
fi

echo "--- Smoke Test Passed Successfully ---"
