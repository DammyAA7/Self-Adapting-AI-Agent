#!/usr/bin/env python3
"""
Cleanup utility for resetting the Self-Adapting AI Agent system.
Ensures clean state for each function generation run.
"""

import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Utilities.write_to_file import clear_file, write_to_file


def reset_for_new_run(clear_generated=False, verbose=True):
    """
    Reset the system for a new function generation run.
    
    Args:
        clear_generated (bool): If True, also clear previously generated functions
                               from functions.py and tools.json
        verbose (bool): If True, print status messages
        
    Returns:
        bool: True if cleanup was successful, False otherwise
    """
    try:
        if verbose:
            print("🧹 Starting system cleanup...")
        
        # Always clear test files
        clear_file('Test_Driven_Development/testDrivenCases.py')
        if verbose:
            print("  ✓ Cleared TDD test cases")
        
        clear_file('Unit_Test/unitTest.py')
        if verbose:
            print("  ✓ Cleared unit tests")
        
        # Reset Unit_Test/functions.py to only contain enums
        enum_content = """from enum import Enum

class Status(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class Priority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
"""
        
        # Clear first, then write to avoid duplicates
        clear_file('Unit_Test/functions.py')
        write_to_file('python', 'Unit_Test/functions.py', enum_content)
        if verbose:
            print("  ✓ Reset Unit_Test/functions.py to enums only")
        
        # Optionally clear generated functions
        if clear_generated:
            # Reset functions.py
            base_functions_content = """# Dynamically generated functions will be added here

if __name__ == "__main__":
    pass"""
            clear_file('functions.py')
            write_to_file('python', 'functions.py', base_functions_content)
            if verbose:
                print("  ✓ Cleared generated functions from functions.py")
            
            # Reset tools.json to empty array
            clear_file('Tool_Descriptor_Gen/tools.json')
            write_to_file('json', 'Tool_Descriptor_Gen/tools.json', '[]')
            if verbose:
                print("  ✓ Reset tools.json to empty array")
        else:
            if verbose:
                print("  ℹ Keeping existing generated functions (use --clean-all to remove)")
        
        if verbose:
            print("✅ Cleanup complete! System ready for new function generation.")
        
        return True
        
    except Exception as e:
        if verbose:
            print(f"❌ Cleanup failed: {e}")
        return False


def cleanup_terminal_context(verbose=True):
    """
    Additional cleanup for terminal context if needed.
    
    Args:
        verbose (bool): If True, print status messages
    """
    try:
        # Check if terminal context is available
        from Terminal_Context.context_manager import get_context_manager
        
        if verbose:
            print("🔄 Cleaning up terminal context...")
        
        context_manager = get_context_manager()
        context_manager.clear_all_contexts()
        
        if verbose:
            print("  ✓ Cleared all terminal contexts")
        
        return True
        
    except ImportError:
        if verbose:
            print("  ℹ Terminal context not available")
        return False
    except Exception as e:
        if verbose:
            print(f"  ⚠ Could not clear terminal context: {e}")
        return False


def full_cleanup(verbose=True):
    """
    Perform a complete system cleanup including all generated content.
    
    Args:
        verbose (bool): If True, print status messages
        
    Returns:
        bool: True if cleanup was successful
    """
    if verbose:
        print("\n" + "="*60)
        print("FULL SYSTEM CLEANUP")
        print("="*60)
    
    # Reset all files including generated functions
    success = reset_for_new_run(clear_generated=True, verbose=verbose)
    
    # Also cleanup terminal context
    cleanup_terminal_context(verbose=verbose)
    
    if verbose:
        print("="*60 + "\n")
    
    return success


if __name__ == "__main__":
    # Command-line interface for cleanup
    import argparse
    
    parser = argparse.ArgumentParser(description='Cleanup utility for Self-Adapting AI Agent')
    parser.add_argument('--full', action='store_true', 
                       help='Perform full cleanup including generated functions')
    parser.add_argument('--quiet', action='store_true',
                       help='Suppress output messages')
    
    args = parser.parse_args()
    
    verbose = not args.quiet
    
    if args.full:
        full_cleanup(verbose=verbose)
    else:
        reset_for_new_run(clear_generated=False, verbose=verbose)