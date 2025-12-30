"""
Hugging Face API Example
Demonstrates: Functions, Classes, API calls, JSON, File Handling
"""

import os
import json
import requests
from dotenv import load_dotenv


# Function example
def save_response_to_file(response_data, filename="huggingface_response.json"):
    """Save API response to a JSON file"""
    with open(filename, 'w') as f:
        json.dump(response_data, f, indent=2)
    print(f"Response saved to {filename}")


# Class example
class HuggingFaceAssistant:
    """A simple class to interact with Hugging Face API"""

    def __init__(self, api_key=None):
        """Initialize with API key from environment or parameter"""
        self.api_key = api_key or os.getenv("HUGGINGFACE_API_KEY")
        if not self.api_key:
            raise ValueError("API key not found. Set HUGGINGFACE_API_KEY environment variable.")
        self.headers = {"Authorization": f"Bearer {self.api_key}"}
        self.api_url = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1"

    def send_message(self, message):
        """Send a message to Hugging Face API and get response"""
        try:
            # Prepare the payload (JSON data)
            payload = {
                "inputs": message,
                "parameters": {
                    "max_new_tokens": 100,
                    "temperature": 0.7
                }
            }

            # Make API request
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json=payload
            )

            # Check if request was successful
            if response.status_code == 200:
                result = response.json()
                return result[0]['generated_text'] if isinstance(result, list) else result
            else:
                return f"Error: {response.status_code} - {response.text}"

        except Exception as e:
            return f"Error: {str(e)}"


def main():
    """Main function to demonstrate API usage"""
    # Load environment variables from .env file
    load_dotenv()

    print("=== Hugging Face API Example ===\n")

    # Create assistant instance
    try:
        assistant = HuggingFaceAssistant()

        # Send a simple message
        message = "Hi"
        print(f"Sending message: '{message}'")

        response = assistant.send_message(message)
        print(f"\nResponse: {response}\n")

        # Save response to file (File Handling + JSON)
        response_data = {
            "input": message,
            "output": response
        }
        save_response_to_file(response_data)

    except ValueError as e:
        print(f"Setup Error: {e}")
        print("\nTo use this script:")
        print("1. Get your API key from https://huggingface.co/settings/tokens")
        print("2. Copy .env.example to .env: cp .env.example .env")
        print("3. Add your API key to the .env file")
        print("4. Run the script again")


if __name__ == "__main__":
    main()
