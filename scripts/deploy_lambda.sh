#!/usr/bin/env bash
set -e

echo "Building SAM application..."
sam build

echo "Deploying to AWS Lambda..."
sam deploy \
  --stack-name crewai-research-pipeline \
  --capabilities CAPABILITY_IAM \
  --parameter-overrides \
    GoogleApiKey=$GOOGLE_API_KEY \
    TavilyApiKey=$TAVILY_API_KEY \
    LangchainApiKey=$LANGCHAIN_API_KEY \
  --region ${AWS_REGION:-eu-central-1}

echo "Deployment complete!"
