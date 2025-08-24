"""
Setup test environment and verify prerequisites
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

def setup_test_environment():
    """Setup and verify test environment"""
    print("Setting up test environment...")
    
    # First check if API key is already set (from main.py)
    openai_key = os.getenv("OPENAI_API_KEY")
    
    if not openai_key:
        # Try to load from .env file if it exists
        env_path = Path('.env')
        if env_path.exists():
            load_dotenv()
            openai_key = os.getenv("OPENAI_API_KEY")
            print("✓ Loaded .env file")
        else:
            # API key might be set in main.py, so we'll set it here temporarily
            # This is the key from main.py
            os.environ["OPENAI_API_KEY"] = "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"
            openai_key = os.getenv("OPENAI_API_KEY")
            print("✓ Using API key from main.py configuration")
    
    if not openai_key or openai_key == "your_openai_api_key_here":
        print("❌ OPENAI_API_KEY not properly set")
        return False
    
    # We don't need Anthropic key anymore since we're using OpenAI only
    print("✓ OpenAI API key configured (OpenAI-only mode)")
    print("ℹ️  No Anthropic API needed - using OpenAI for all operations")
    
    # # Clean up any existing test artifacts
    # cleanup_files = [
    #     'Unit_Test/unitTest.py',
    #     'Unit_Test/functions.py',
    #     'Test_Driven_Development/testDrivenCases.py'
    # ]
    #
    # for file in cleanup_files:
    #     file_path = Path(file)
    #     if file_path.exists():
    #         try:
    #             os.remove(file_path)
    #             print(f"  Cleaned: {file}")
    #         except Exception as e:
    #             print(f"  Warning: Could not clean {file}: {e}")
    
    # Ensure required directories exist
    required_dirs = [
        'Unit_Test',
        'Test_Driven_Development',
        'Utilities',
        'Core',
        'Function_Gen',
        'Adjudicator',
        'Tool_Descriptor_Gen',
        'Prompt_Gen',
        'Intermidiate_Adjudicator'
    ]
    
    for dir_name in required_dirs:
        dir_path = Path(dir_name)
        if not dir_path.exists():
            print(f"❌ Required directory missing: {dir_name}")
            return False
    
    print("✓ All required directories present")
    
    # Check for required files
    required_files = [
        'Core/main.py',
        'functions.py',
        'Tool_Descriptor_Gen/tools.json',
        'Core/prompt.txt'
    ]
    
    for file_name in required_files:
        file_path = Path(file_name)
        if not file_path.exists():
            print(f"❌ Required file missing: {file_name}")
            return False
    
    print("✓ All required files present")
    print("✓ Test environment ready")
    return True

if __name__ == "__main__":
    if setup_test_environment():
        print("\n✅ Environment setup complete. You can now run tests.")
    else:
        print("\n❌ Environment setup failed. Please fix the issues above.")
        sys.exit(1)