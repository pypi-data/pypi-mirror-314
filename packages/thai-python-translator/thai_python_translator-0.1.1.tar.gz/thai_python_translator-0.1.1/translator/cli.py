"""
Command Line Interface for Thai Python Translator.

This module provides the command-line interface for executing Thai Python code files.
It allows users to run Thai Python scripts directly from the command line using
the 'thai-python' command.

Usage:
    thai-python <script.py>

Examples:
    $ thai-python examples/hello_thai.py
    $ thai-python examples/advanced_thai.py
"""

from translator.core import execute_translated_code

def main():
    """
    Main entry point for the Thai Python CLI.

    This function handles command-line arguments and executes Thai Python files.
    It expects a single argument specifying the path to a Thai Python script file.

    The script file should contain valid Thai Python code. The function will:
    1. Read the contents of the specified file
    2. Translate the Thai Python code to standard Python
    3. Execute the translated code
    4. Display any output or error messages in Thai

    Returns:
        None. Exits with status code 1 if an error occurs, 0 otherwise.

    Example:
        Given a file 'hello.py' with contents:
            ฟังก์ชัน ทักทาย():
                พิมพ์("สวัสดี!")
            ทักทาย()

        Running:
            $ thai-python hello.py
        
        Will output:
            สวัสดี!
    """
    import sys
    if len(sys.argv) < 2:
        print("Usage: thai-python <script.py>")
        sys.exit(1)

    script_path = sys.argv[1]
    try:
        with open(script_path, "r", encoding="utf-8") as script_file:
            thai_code = script_file.read()
        
        execute_translated_code(thai_code)
    except FileNotFoundError:
        print(f"Error: Could not find file '{script_path}'")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()