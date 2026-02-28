#!/bin/bash
# Helper script to deploy the BlueBullFly Marketing Portal to Cloud Run

GCP_PROJECT_ID="bluebullfly-5cc16"
GCP_REGION="us-central1"
GCP_DEPLOY_SERVICE_NAME="marketing-portal"
IMAGE_URL="gcr.io/${GCP_PROJECT_ID}/${GCP_DEPLOY_SERVICE_NAME}"

echo "Building Next.js Docker image..."
# Notice the --platform linux/amd64 flag required by Cloud Run
docker build --platform linux/amd64 -t $IMAGE_URL .

echo "Pushing image to GCP Artifact Registry / GCR..."
docker push $IMAGE_URL

echo "Deploying to Cloud Run Service..."
gcloud run deploy $GCP_DEPLOY_SERVICE_NAME \
    --image $IMAGE_URL \
    --GCP_REGION $GCP_REGION \
    --project $GCP_PROJECT_ID \
    --allow-unauthenticated \
    --port 3000

echo "Deployment complete! Your Portal is ready."
