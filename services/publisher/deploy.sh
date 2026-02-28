#!/bin/bash
# Helper script to deploy the Publishing API Connector as a Cloud Run Service
# Requires HTTP listening for the TikTok OAuth callback.

GCP_PROJECT_ID="bluebullfly-5cc16"
GCP_REGION="us-central1"
GCP_DEPLOY_SERVICE_NAME="publisher-api"
IMAGE_URL="gcr.io/${GCP_PROJECT_ID}/${GCP_DEPLOY_SERVICE_NAME}"

echo "Building Docker image for linux/amd64..."
docker build --platform linux/amd64 -t $IMAGE_URL .

echo "Pushing image to GCP Artifact Registry / GCR..."
docker push $IMAGE_URL

echo "Deploying to Cloud Run Service..."
gcloud run deploy $GCP_DEPLOY_SERVICE_NAME \
    --image $IMAGE_URL \
    --GCP_REGION $GCP_REGION \
    --project $GCP_PROJECT_ID \
    --allow-unauthenticated \
    --timeout 3600 \
    --set-env-vars=GCP_BUCKET_NAME=bluebullfly-assets

echo "Deployment complete!"
echo "To map your custom domain, run:"
echo "gcloud run domain-mappings create --service $GCP_DEPLOY_SERVICE_NAME --domain api.bluebullfly.com --GCP_REGION $GCP_REGION --project $GCP_PROJECT_ID"
