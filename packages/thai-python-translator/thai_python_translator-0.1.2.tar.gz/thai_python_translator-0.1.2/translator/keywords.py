# translator/keywords.py
"""
Thai to Python keyword and operator mappings.

This module contains dictionaries that map Thai programming keywords and operators
to their Python equivalents. These mappings are used by the translator to convert
Thai Python code to standard Python code.
"""

KEYWORD_MAP = {
    # Control flow
    "ฟังก์ชัน": "def",      # Function definition
    "คลาส": "class",      # Class definition
    "ผ่าน": "pass",       # Pass statement
    "ส่งคืน": "return",     # Return statement
    "ถ้า": "if",           # If condition
    "ไม่งั้น": "else",      # Else clause
    "หรือถ้า": "elif",      # Else if condition
    "สำหรับ": "for",       # For loop
    "ใน": "in",           # In operator
    "ขณะที่": "while",     # While loop
    "หยุด": "break",      # Break loop
    "ทำต่อ": "continue",   # Continue loop
    "พยายาม": "try",       # Try block
    "จับข้อผิดพลาด": "except", # Except block
    "ท้ายที่สุด": "finally",  # Finally block
    "นำเข้า": "import",    # Import statement
    
    # Boolean values
    "จริง": "True",        # Boolean True
    "เท็จ": "False",       # Boolean False
    "ไม่มี": "None",       # None value
    
    # Built-in functions
    "พิมพ์": "print",      # Print function
    "รับค่า": "input",     # Input function
    "ช่วง": "range",      # Range function
    "รายการ": "list",     # List constructor
    "พจนานุกรม": "dict",   # Dictionary constructor
    "เซต": "set",        # Set constructor
    "ตัวเลข": "int",      # Integer constructor
    "ทศนิยม": "float",    # Float constructor
    "ข้อความ": "str",     # String constructor
    "ความยาว": "len",     # Length function
    "ฟังก์ชันย่อย": "lambda", # Lambda function
    "คืนค่า": "yield",    # Yield statement
    "ทั่วไป": "global",   # Global statement
    "ตัวเอง": "self",     # Self reference
}

OPERATOR_MAP = {
    # Arithmetic operators
    "บวก": "+",           # Addition
    "ลบ": "-",           # Subtraction
    "คูณ": "*",          # Multiplication
    "หาร": "/",          # Division
    "ลบออก": "del",      # Delete operator
    
    # Logical operators
    "และ": "and",        # Logical AND
    "หรือ": "or",        # Logical OR
    "ไม่": "not",        # Logical NOT
    
    # Comparison operators
    "เท่ากับ": "==",      # Equal to
    "ไม่เท่ากับ": "!=",    # Not equal to
    "มากกว่า": ">",       # Greater than
    "น้อยกว่า": "<",      # Less than
    "มากกว่าเท่ากับ": ">=", # Greater than or equal to
    "น้อยกว่าเท่ากับ": "<=", # Less than or equal to
}

METHOD_MAP = {
    # List methods
    "เพิ่ม": "append",     # Append to list
    "นำออก": "pop",       # Pop from list
    "แทรก": "insert",    # Insert into list
    "ลบ": "remove",      # Remove from list
    
    # File operations
    "เปิด": "open",       # Open file
    "ปิด": "close",      # Close file
    "อ่าน": "read",      # Read file
    "เขียน": "write",     # Write file
    
    # String methods
    "แยก": "split",      # Split string
    "ต่อ": "join",       # Join string
    "แทนที่": "replace",  # Replace in string
    
    # Dict methods
    "หาค่า": "get",       # Get dict value
    "ค่าทั้งหมด": "values", # Dict values
    "คีย์ทั้งหมด": "keys"   # Dict keys
}