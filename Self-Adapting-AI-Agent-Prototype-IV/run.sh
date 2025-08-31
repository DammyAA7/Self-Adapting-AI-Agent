#!/bin/bash

# Set Azure OpenAI credentials (replace with your actual key)
export AZURE_OPENAI_API_KEY="your_azure_api_key_here"
export AZURE_OPENAI_ENDPOINT="https://jenly-staging.cognitiveservices.azure.com"
export AZURE_OPENAI_API_VERSION="2024-12-01-preview"

# Run the application
python Core/main.py