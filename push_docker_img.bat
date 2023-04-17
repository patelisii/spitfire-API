export PROJECT_ID=spitfire-api
export IMAGE_NAME=spitfire
docker build --platform linux/amd64 -t patelisii/spitfire .
docker build -t gcr.io/$PROJECT_ID/$IMAGE_NAME .
docker push gcr.io/$PROJECT_ID/$IMAGE_NAME
/Users/patrickelisii/google-cloud-sdk/bin/gcloud run deploy spitfire-api-1 \
    --image gcr.io/$PROJECT_ID/$IMAGE_NAME \
    --platform managed \
    --region us-east1 \
    --allow-unauthenticated
