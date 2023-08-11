# Define variables
export MICROSOFT_RESOURCE_GROUP="CHANGE_THIS"
export MICROSOFT_APP_NAME="CHANGE_THIS"
export GOOGLE_APPLICATION_CREDENTIALS="CHANGE_THIS"
export CRUN_GENAI_SERVICE_SA="CHANGE_THIS"
export CRUN_GENAI_SERVICE_URL="CHANGE_THIS"
export PROJECT_ID="CHANGE_THIS"
export SEARCH_ENGINE_ID="CHANGE_THIS"

# Create the zip file with the app code
rm "${MICROSOFT_APP_NAME}.zip"
zip -r "${MICROSOFT_APP_NAME}.zip" . -x '.??*'

# Set the app settings
az webapp config appsettings set \
    --resource-group "${MICROSOFT_RESOURCE_GROUP}" \
    --name "${MICROSOFT_APP_NAME}" \
    --settings SCM_DO_BUILD_DURING_DEPLOYMENT=true

az webapp config appsettings set \
    --resource-group "${MICROSOFT_RESOURCE_GROUP}" \
    --name "${MICROSOFT_APP_NAME}" \
    --settings WEBSITES_CONTAINER_START_TIME_LIMIT=1800

az webapp config appsettings set \
    --resource-group "${MICROSOFT_RESOURCE_GROUP}" \
    --name "${MICROSOFT_APP_NAME}" \
    --settings GOOGLE_APPLICATION_CREDENTIALS="${GOOGLE_APPLICATION_CREDENTIALS}"

az webapp config appsettings set \
    --resource-group "${MICROSOFT_RESOURCE_GROUP}" \
    --name "${MICROSOFT_APP_NAME}" \
    --settings CRUN_GENAI_SERVICE_SA="${CRUN_GENAI_SERVICE_SA}"

az webapp config appsettings set \
    --resource-group "${MICROSOFT_RESOURCE_GROUP}" \
    --name "${MICROSOFT_APP_NAME}" \
    --settings CRUN_GENAI_SERVICE_URL="${CRUN_GENAI_SERVICE_URL}"

az webapp config appsettings set \
    --resource-group "${MICROSOFT_RESOURCE_GROUP}" \
    --name "${MICROSOFT_APP_NAME}" \
    --settings PROJECT_ID="${PROJECT_ID}"

az webapp config appsettings set \
    --resource-group "${MICROSOFT_RESOURCE_GROUP}" \
    --name "${MICROSOFT_APP_NAME}" \
    --settings SEARCH_ENGINE_ID="${SEARCH_ENGINE_ID}"

echo "Waiting 10 seconds before deploying the bot"
sleep 10
az webapp deployment source config-zip \
    --resource-group "${MICROSOFT_RESOURCE_GROUP}" \
    --name "${MICROSOFT_APP_NAME}" --src "./${MICROSOFT_APP_NAME}.zip"