#!/bin/bash
# Helper script to deploy the Unified Data Warehouse ETL as a Cloud Run Service
# Triggers via HTTP (which Cloud Scheduler will hit nightly)

PROJECT_ID="bluebullfly-5cc16"
REGION="us-central1"
SERVICE_NAME="data-warehouse-etl"
IMAGE_URL="gcr.io/${PROJECT_ID}/${SERVICE_NAME}"

echo "Building Docker image for linux/amd64..."
docker build --platform linux/amd64 -t $IMAGE_URL .

echo "Pushing image to GCP Artifact Registry / GCR..."
docker push $IMAGE_URL

echo "Deploying to Cloud Run Service..."
gcloud run deploy $SERVICE_NAME \
    --image $IMAGE_URL \
    --region $REGION \
    --project $PROJECT_ID \
    --allow-unauthenticated \
    --timeout 3600

echo "Deployment complete!"
echo "Make sure all environment variables are set in GCP Console (Secret Manager or ENV overrides)."
