'''
Function that generates tool definitions based on a prompt using OpenAI's API.
Handles both single functions and multiple functions, returning a properly formatted JSON array.
'''
import json

def generate_tool_definitions(client, function_code):
    with open('Tool_Descriptor_Gen/tools.txt', 'r') as f:
        generator_prompt = f.read()
    
    generator_messages = [
        {"role": "system", "content": generator_prompt},
        {"role": "user", "content": f"Generate tool descriptors for ALL functions in this code:\n\n{function_code}"}
    ]

    generator_response = client.chat.completions.create(
        model="gpt-4.1",  # Azure deployment name
        messages=generator_messages
    )

    tools_response = generator_response.choices[0].message.content.strip()
    
    try:
        # Parse the JSON to ensure it's valid
        parsed_tools = json.loads(tools_response)
        
        # Ensure it's always an array
        if not isinstance(parsed_tools, list):
            parsed_tools = [parsed_tools]
        
        # Log the generated functions for debugging
        function_names = [tool.get('function', {}).get('name', 'unknown') for tool in parsed_tools]
        print(f"Generated tool descriptors for: {', '.join(function_names)}")
        
        # Return formatted JSON
        return json.dumps(parsed_tools, indent=4)
        
    except json.JSONDecodeError as e:
        print(f"Warning: Could not parse tool descriptor JSON: {e}")
        print(f"Raw response: {tools_response}")
        
        # Fallback: try to fix common issues
        if tools_response.strip().startswith('{') and not tools_response.strip().startswith('['):
            # Single object, wrap in array
            try:
                single_tool = json.loads(tools_response)
                return json.dumps([single_tool], indent=4)
            except:
                pass
        
        # If all else fails, return empty array
        return "[]"