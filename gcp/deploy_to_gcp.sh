# Define variables
export CRUN_SERVICE_NAME="CHANGE_THIS"
export REGION="CHANGE_THIS"
export PROJECT_ID="CHANGE_THIS"

# Deploy the cloud-run service
gcloud run deploy "${CRUN_SERVICE_NAME}" \
    --region="${REGION}" \
    --project="${PROJECT_ID}" \
    --source .