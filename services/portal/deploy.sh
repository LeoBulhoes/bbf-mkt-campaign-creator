#!/bin/bash
# Helper script to deploy the BlueBullFly Marketing Portal to Cloud Run

PROJECT_ID="bluebullfly-5cc16"
REGION="us-central1"
SERVICE_NAME="marketing-portal"
IMAGE_URL="gcr.io/${PROJECT_ID}/${SERVICE_NAME}"

echo "Building Next.js Docker image..."
# Notice the --platform linux/amd64 flag required by Cloud Run
docker build --platform linux/amd64 -t $IMAGE_URL .

echo "Pushing image to GCP Artifact Registry / GCR..."
docker push $IMAGE_URL

echo "Deploying to Cloud Run Service..."
gcloud run deploy $SERVICE_NAME \
    --image $IMAGE_URL \
    --region $REGION \
    --project $PROJECT_ID \
    --allow-unauthenticated \
    --port 3000

echo "Deployment complete! Your Portal is ready."
