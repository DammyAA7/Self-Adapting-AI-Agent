# Setup Instructions

## Environment Variables

This project requires Azure OpenAI API credentials to be set as environment variables.

### Option 1: Using .env file (Recommended for development)

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your Azure OpenAI credentials:
   ```
   AZURE_OPENAI_API_KEY=your_actual_api_key_here
   AZURE_OPENAI_ENDPOINT=https://your-resource.cognitiveservices.azure.com
   AZURE_OPENAI_API_VERSION=2024-12-01-preview
   ```

3. Update `Core/main.py` to load the .env file by uncommenting line 42:
   ```python
   load_dotenv()  # Uncomment this line
   ```

### Option 2: Export environment variables

```bash
export AZURE_OPENAI_API_KEY="your_api_key_here"
export AZURE_OPENAI_ENDPOINT="https://your-resource.cognitiveservices.azure.com"
export AZURE_OPENAI_API_VERSION="2024-12-01-preview"
```

### Option 3: Set in your IDE

If using PyCharm or VS Code, you can set environment variables in your run configuration.

## Important Security Notes

- **NEVER** commit your actual API keys to version control
- Always use environment variables or `.env` files (which should be in `.gitignore`)
- The `.env` file is already included in `.gitignore` to prevent accidental commits

## Running the Application

After setting up your environment variables:

```bash
cd Self-Adapting-AI-Agent-Prototype-IV
python Core/main.py
```