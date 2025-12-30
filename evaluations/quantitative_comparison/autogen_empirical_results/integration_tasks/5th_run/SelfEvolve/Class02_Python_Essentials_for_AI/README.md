# Class 02: Python Essentials for AI Applications

## Course Topics Overview

### 1. Functions
- **Definition**: Reusable blocks of code that perform specific tasks
- **Benefits**: Code organization, reusability, and maintainability
- **Syntax**:
  ```python
  def function_name(parameters):
      # code block
      return result
  ```
- **Examples in our scripts**:
  - `save_response_to_file()` - saves data to JSON files
  - `send_message()` - handles API communication

### 2. Classes
- **Definition**: Blueprints for creating objects with attributes and methods
- **Object-Oriented Programming**: Organizes code around data and functionality
- **Key Concepts**:
  - `__init__()` - Constructor method
  - `self` - Reference to instance
  - Methods - Functions inside a class
- **Examples in our scripts**:
  - `OpenAIAssistant` - Manages OpenAI API interactions
  - `HuggingFaceAssistant` - Manages Hugging Face API interactions

### 3. API Calls
- **What is an API**: Application Programming Interface - way for programs to communicate
- **REST APIs**: Send HTTP requests and receive responses
- **Common Methods**:
  - GET - Retrieve data
  - POST - Send data
- **Authentication**: API keys for secure access

### 4. JSON (JavaScript Object Notation)
- **Purpose**: Lightweight data format for data exchange
- **Structure**: Key-value pairs, similar to Python dictionaries
- **Common Operations**:
  - `json.dump()` - Write JSON to file
  - `json.load()` - Read JSON from file
  - `json.dumps()` - Convert to JSON string
  - `json.loads()` - Parse JSON string
- **Usage**: API requests/responses, configuration files, data storage

### 5. File Handling
- **Opening Files**: `open(filename, mode)`
- **Modes**:
  - `'r'` - Read
  - `'w'` - Write (overwrites)
  - `'a'` - Append
- **Best Practice**: Use `with` statement for automatic file closing
  ```python
  with open('file.txt', 'w') as f:
      f.write('data')
  ```

### 6. Working with External APIs
- **requests Library**: Python HTTP library for API calls
- **Basic Workflow**:
  1. Import requests
  2. Prepare headers (authentication)
  3. Prepare payload (data to send)
  4. Send request (`requests.post()`, `requests.get()`)
  5. Handle response
- **Response Handling**:
  - `response.status_code` - Check if successful (200 = OK)
  - `response.json()` - Parse JSON response
  - `response.text` - Get raw text

### 7. Virtual Environments & Requirements
- **Virtual Environment**: Isolated Python environment for each project
- **Why Use**:
  - Avoid dependency conflicts
  - Project-specific package versions
  - Easy deployment
- **Two Popular Options**:

  **Option 1: venv (Built-in Python)**
  ```bash
  python -m venv venv          # Create
  source venv/bin/activate     # Activate (Linux/Mac)
  venv\Scripts\activate        # Activate (Windows)
  pip install -r requirements.txt  # Install dependencies
  deactivate                   # Deactivate
  ```

  **Option 2: conda (Anaconda/Miniconda)**
  ```bash
  conda create -n myenv python=3.10  # Create
  conda activate myenv               # Activate
  pip install -r requirements.txt    # Install dependencies
  conda deactivate                   # Deactivate
  ```

- **requirements.txt**: Lists all project dependencies

---

## Project Files

### 1. `openai_example.py`
**Purpose**: Demonstrates OpenAI API integration

**Key Features**:
- **Class**: `OpenAIAssistant` - manages API client and requests
- **Function**: `save_response_to_file()` - saves responses to JSON
- **API Call**: Uses OpenAI's chat completion endpoint
- **File Handling**: Writes JSON response to file
- **Environment Variables**: Securely loads API key

**What it does**:
- Sends "Hi" message to OpenAI GPT model
- Receives AI-generated response
- Saves response to `openai_response.json`

### 2. `huggingface_example.py`
**Purpose**: Demonstrates Hugging Face API integration using requests library

**Key Features**:
- **Class**: `HuggingFaceAssistant` - manages API communication
- **Function**: `save_response_to_file()` - saves responses to JSON
- **API Call**: Uses requests library to call Hugging Face Inference API
- **JSON Handling**: Sends and receives JSON data
- **Error Handling**: Checks status codes and handles exceptions

**What it does**:
- Sends "Hi" message to Mistral-7B model via Hugging Face
- Receives AI-generated response
- Saves input/output to `huggingface_response.json`

### 3. `requirements.txt`
**Purpose**: Lists all Python packages needed for the project

**Contents**:
- `openai>=1.0.0` - Official OpenAI Python client
- `requests>=2.31.0` - HTTP library for API calls
- `python-dotenv>=1.0.0` - Loads environment variables from .env file

### 4. `.env.example`
**Purpose**: Template file for environment variables

**What it does**:
- Shows which API keys are needed
- Provides a template to create your own `.env` file
- Keeps sensitive API keys out of version control

---

## Setup Instructions

### Step 1: Create Virtual Environment

**Option A: Using venv (Built-in)**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

**Option B: Using conda**
```bash
conda create -n class02 python=3.10
conda activate class02
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Set Up API Keys

1. **Copy the example environment file**:
   ```bash
   cp .env.example .env
   ```

2. **Get your API keys**:
   - **OpenAI**: https://platform.openai.com/api-keys
   - **Hugging Face**: https://huggingface.co/settings/tokens

3. **Edit the `.env` file** and add your API keys:
   ```
   OPENAI_API_KEY=your-actual-openai-key-here
   HUGGINGFACE_API_KEY=your-actual-huggingface-key-here
   ```

**Note**: The `.env` file should NOT be committed to version control (add it to `.gitignore`)

### Step 4: Run the Scripts
```bash
python openai_example.py
python huggingface_example.py
```

---

## Expected Output

### openai_example.py
```
=== OpenAI API Example ===

Sending message: 'Hi'

Response: Hello! How can I assist you today?

Response saved to openai_response.json
```

### huggingface_example.py
```
=== Hugging Face API Example ===

Sending message: 'Hi'

Response: Hi Hello! How can I assist you today?

Response saved to huggingface_response.json
```

---

## Key Takeaways

1. **Functions** make code reusable and organized
2. **Classes** group related data and functions together
3. **APIs** allow programs to communicate and access external services
4. **JSON** is the standard format for API data exchange
5. **File Handling** enables persistent data storage
6. **requests library** simplifies HTTP API calls
7. **Virtual Environments** keep projects isolated and manageable
8. **Environment Variables** store sensitive data like API keys securely
9. **python-dotenv** loads environment variables from `.env` files automatically

---

## Common Errors & Solutions

**Error**: `ModuleNotFoundError: No module named 'openai'` or `'dotenv'`
- **Solution**: Run `pip install -r requirements.txt`

**Error**: `API key not found`
- **Solution**: Create `.env` file from `.env.example` and add your API keys

**Error**: `.env` file not being read
- **Solution**: Make sure `.env` file is in the same directory as the script

**Error**: `429 Rate Limit` or `503 Service Unavailable`
- **Solution**: Wait a moment and try again (API quota or server issue)

---

## Further Practice

1. Modify the message sent to the APIs
2. Try different OpenAI models (gpt-4, gpt-4-turbo)
3. Try different Hugging Face models
4. Add more parameters (temperature, max_tokens)
5. Create a function to read saved JSON files
6. Add error logging to a file
7. Create a simple chatbot loop
