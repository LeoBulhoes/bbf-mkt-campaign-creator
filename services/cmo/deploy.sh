#!/bin/bash
# Helper script to deploy the BlueBullFly AI CMO Agent to Cloud Run

PROJECT_ID="bluebullfly-5cc16"
REGION="us-central1"
SERVICE_NAME="ai-cmo-agent"
IMAGE_URL="gcr.io/${PROJECT_ID}/${SERVICE_NAME}"

echo "Building Docker image for linux/amd64..."
docker build --platform linux/amd64 -t $IMAGE_URL .

echo "Pushing image to GCP Artifact Registry / GCR..."
docker push $IMAGE_URL

echo "Deploying to Cloud Run Service..."
# Note: Given this is an AI agent that hits multiple external APIs, 
# we increase the timeout to 3600s (1 hour) just in case.
gcloud run deploy $SERVICE_NAME \
    --image $IMAGE_URL \
    --region $REGION \
    --project $PROJECT_ID \
    --allow-unauthenticated \
    --timeout 3600

echo "Deployment complete!"
echo "Make sure all environment variables are set in GCP Console (Secret Manager or ENV overrides)."
echo " - GOOGLE_API_KEY"
echo " - META_APP_ID, META_APP_SECRET, META_ACCESS_TOKEN"
