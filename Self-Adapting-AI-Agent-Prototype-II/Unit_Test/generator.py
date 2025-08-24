"""
This script generates a prompt for creating unit tests for a function.
"""

# Read the new prompt from file
with open('Unit_Test/prompt.txt', 'r') as f:
    generator_prompt = f.read()

def generateTestCases(client, requirements):
    generator_messages = [
        {"role": "assistant", "content": generator_prompt},
        {"role": "user", "content":  requirements}
    ]

    generator_response = client.messages.create(
    model="claude-3-7-sonnet-20250219",
    max_tokens=3000,
    messages=generator_messages,
    )
     
    return generator_response.content[0].text