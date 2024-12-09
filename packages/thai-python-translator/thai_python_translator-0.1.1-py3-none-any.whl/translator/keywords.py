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
    "ส่งคืน": "return",     # Return statement
    "ถ้า": "if",           # If condition
    "ทำอีก": "else",       # Else clause
    "หรือถ้า": "elif",      # Else if condition
    "สำหรับ": "for",       # For loop
    "ใน": "in",           # In operator
    "ขณะที่": "while",     # While loop
    "พยายาม": "try",       # Try block
    "จับข้อผิดพลาด": "except", # Except block
    "ท้ายที่สุด": "finally",  # Finally block
    
    # Boolean values
    "จริง": "True",        # Boolean True
    "เท็จ": "False",       # Boolean False
    "ไม่มี": "None",       # None value
    
    # Built-in functions
    "พิมพ์": "print",      # Print function
    "ช่วง": "range",      # Range function
    "รายการ": "list",     # List constructor
    "พจนานุกรม": "dict",   # Dictionary constructor
    "เซต": "set",        # Set constructor
    "ตัวเลข": "int",      # Integer constructor
    "ทศนิยม": "float",    # Float constructor
    "ข้อความ": "str",     # String constructor
    "ความยาว": "len",     # Length function
}

OPERATOR_MAP = {
    # Arithmetic operators
    "บวก": "+",           # Addition
    "ลบ": "-",           # Subtraction
    "คูณ": "*",          # Multiplication
    "หาร": "/",          # Division
    
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