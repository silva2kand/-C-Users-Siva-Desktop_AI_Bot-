#!/usr/bin/env python3
"""
Example: Running Tests and Validation
Demonstrates how to run tests and validate the application
"""

import subprocess
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))


def run_command(command, description):
    """Run a command and display results"""
    print(f"Running: {description}")
    print(f"Command: {command}")
    print("-" * 50)
    
    try:
        result = subprocess.run(
            command, shell=True, capture_output=True, text=True, cwd=os.path.dirname(__file__) + "/../.."
        )
        
        if result.returncode == 0:
            print("✓ SUCCESS")
            if result.stdout:
                print("Output:")
                print(result.stdout[:500] + ("..." if len(result.stdout) > 500 else ""))
        else:
            print("✗ FAILED")
            if result.stderr:
                print("Error:")
                print(result.stderr[:500] + ("..." if len(result.stderr) > 500 else ""))
    
    except Exception as e:
        print(f"✗ ERROR: {e}")
    
    print("\n" + "="*60 + "\n")


def main():
    print("=== Test and Validation Example ===\n")
    
    # Check if we're in the right directory
    if not os.path.exists("src/main.py"):
        print("Error: Please run this from the project root directory")
        sys.exit(1)
    
    print("This example demonstrates how to validate the application setup.\n")
    
    # 1. Basic import test
    run_command(
        "python -c \"from src.main import FloatingBotsApp; print('✓ All imports successful')\"",
        "Testing imports"
    )
    
    # 2. Configuration test
    run_command(
        "python -c \"from src.config import Config; print(f'✓ Config loaded: {Config.BOT_NAME}')\"",
        "Testing configuration"
    )
    
    # 3. Bot functionality test
    run_command(
        "python -c \"from src.bot import Bot; b=Bot(); r=b.get_response('test'); print(f'✓ Bot response: {r[:30]}...')\"",
        "Testing bot functionality"
    )
    
    # 4. Run unit tests (if available)
    if os.path.exists("tests"):
        run_command(
            "python -m pytest tests/test_config.py tests/test_bot.py -v",
            "Running unit tests"
        )
    
    # 5. Code formatting check
    run_command(
        "python -c \"import black; print('✓ Black formatting tool available')\"",
        "Checking code formatting tools"
    )
    
    # 6. Linting check
    run_command(
        "python -c \"import flake8; print('✓ Flake8 linting tool available')\"",
        "Checking linting tools"
    )
    
    # 7. Application test script
    if os.path.exists("test_app.py"):
        run_command(
            "python test_app.py",
            "Running application test script"
        )
    
    print("=== Validation Complete ===")
    print("\nNext steps:")
    print("1. If all tests pass, the application is ready to use")
    print("2. Run 'python -m src.main' to start the application")
    print("3. Set OPENAI_API_KEY environment variable for AI responses")
    print("4. Use 'pip install -e .' for development installation")


if __name__ == "__main__":
    main()