#!/bin/bash
# ==============================================================================
# SME Academy: Deploy Conversational Analytics Web App to Google Cloud Run
# Target Environment: Student's Google Cloud Argolis Project
# ==============================================================================

set -e

SERVICE_NAME="${SERVICE_NAME:-looker-agentic-web-app}"
REGION="${REGION:-us-central1}"
PROJECT_ID="$(gcloud config get-value project 2>/dev/null)"

if [ -z "$PROJECT_ID" ]; then
  echo "❌ Error: No Google Cloud project configured."
  echo "Please run: gcloud config set project YOUR_ARGOLIS_PROJECT_ID"
  exit 1
fi

echo "============================================================"
echo "🚀 Deploying to Google Cloud Run in Argolis"
echo "Project ID : $PROJECT_ID"
echo "Service    : $SERVICE_NAME"
echo "Region     : $REGION"
echo "============================================================"

# Check for Looker API credentials
LOOKER_BASE_URL="${LOOKER_BASE_URL:-https://ceworkshops.cloud.looker.com}"

if [ -z "$LOOKER_CLIENT_ID" ] || [ -z "$LOOKER_CLIENT_SECRET" ]; then
  if [ -f .env ]; then
    echo "📄 Reading credentials from .env..."
    export $(grep -v '^#' .env | xargs)
  fi
fi

ENV_VARS="LOOKER_BASE_URL=${LOOKER_BASE_URL}"
if [ -n "$LOOKER_CLIENT_ID" ]; then
  ENV_VARS="${ENV_VARS},LOOKER_CLIENT_ID=${LOOKER_CLIENT_ID}"
fi
if [ -n "$LOOKER_CLIENT_SECRET" ]; then
  ENV_VARS="${ENV_VARS},LOOKER_CLIENT_SECRET=${LOOKER_CLIENT_SECRET}"
fi

gcloud run deploy "$SERVICE_NAME" \
  --source . \
  --project "$PROJECT_ID" \
  --region "$REGION" \
  --allow-unauthenticated \
  --set-env-vars "$ENV_VARS"

echo ""
echo "✅ Deployment completed successfully!"
echo "Students can access the interactive lab portal via the Service URL above."
