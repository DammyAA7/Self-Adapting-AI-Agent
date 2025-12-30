"""
OpenAI API Example
Demonstrates: Functions, Classes, API calls, JSON, File Handling
"""

import os
import json
from openai import OpenAI
from dotenv import load_dotenv


# Function example
def save_response_to_file(response_text, filename="openai_response.json"):
    """Save API response to a JSON file"""
    data = {
        "response": response_text,
        "timestamp": "2024"
    }
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"Response saved to {filename}")


# Class example
class OpenAIAssistant:
    """A simple class to interact with OpenAI API"""

    def __init__(self, api_key=None):
        """Initialize with API key from environment or parameter"""
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("API key not found. Set OPENAI_API_KEY environment variable.")
        self.client = OpenAI(api_key=self.api_key)

    def send_message(self, message, model="gpt-3.5-turbo"):
        """Send a message to OpenAI and get response"""
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "user", "content": message}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error: {str(e)}"


def main():
    """Main function to demonstrate API usage"""
    # Load environment variables from .env file
    load_dotenv()

    print("=== OpenAI API Example ===\n")

    # Create assistant instance
    try:
        assistant = OpenAIAssistant()

        # Send a simple message
        message = "Hi"
        print(f"Sending message: '{message}'")

        response = assistant.send_message(message)
        print(f"\nResponse: {response}\n")

        # Save response to file (File Handling + JSON)
        save_response_to_file(response)

    except ValueError as e:
        print(f"Setup Error: {e}")
        print("\nTo use this script:")
        print("1. Get your API key from https://platform.openai.com/api-keys")
        print("2. Copy .env.example to .env: cp .env.example .env")
        print("3. Add your API key to the .env file")
        print("4. Run the script again")


if __name__ == "__main__":
    main()
