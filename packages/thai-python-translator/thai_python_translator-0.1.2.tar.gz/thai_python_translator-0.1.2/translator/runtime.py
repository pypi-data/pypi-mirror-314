# translator/runtime.py
"""
Runtime error handling and translation for Thai Python.

This module provides functionality for translating Python runtime errors into Thai
and customizing the Python exception handling system to display errors in Thai.
"""

import sys
from typing import Any, Type

ERROR_MAP = {
    # Maps Python error types to Thai error messages
    "NameError": "ชื่อที่ระบุไม่มีอยู่ในขอบเขตนี้",          # Name not found in scope
    "SyntaxError": "โครงสร้างของโค้ดไม่ถูกต้อง",           # Invalid code structure
    "TypeError": "ชนิดข้อมูลไม่ถูกต้อง",                   # Invalid data type
    "ValueError": "ค่าไม่ถูกต้อง",                        # Invalid value
    "IndexError": "ดัชนีเกินขอบเขต",                      # Index out of range
    "KeyError": "ไม่พบคีย์ที่ระบุ",                       # Key not found
    "AttributeError": "ไม่พบคุณสมบัติที่ระบุ",              # Attribute not found
    "ZeroDivisionError": "หารด้วยศูนย์",                  # Division by zero
    "ImportError": "นำเข้าโมดูลไม่สำเร็จ",                 # Module import failed
    "FileNotFoundError": "ไม่พบไฟล์ที่ระบุ",              # File not found
}

def translate_error(error: Exception) -> str:
    """
    Translate a Python error message to Thai.

    Args:
        error: The Python exception object to translate

    Returns:
        A Thai error message corresponding to the error type,
        or the original error message if no translation exists.

    Example:
        >>> try:
        ...     x = 1 / 0
        ... except Exception as e:
        ...     print(translate_error(e))
        หารด้วยศูนย์
    """
    error_type = type(error).__name__
    return ERROR_MAP.get(error_type, str(error))

def custom_excepthook(type_: Type[BaseException], value: BaseException, traceback: Any) -> None:
    """
    Custom exception hook that displays error messages in Thai.

    This function replaces the default Python exception handler to provide
    error messages in Thai. It translates the error message and then calls
    the original exception handler.

    Args:
        type_: The type of the exception
        value: The exception instance
        traceback: The traceback object

    Note:
        This function is automatically installed as the system exception
        handler when the module is imported.
    """
    translated_message = translate_error(value)
    print(f"ข้อผิดพลาด: {translated_message}")
    sys.__excepthook__(type_, value, traceback)

# Install the custom exception hook
sys.excepthook = custom_excepthook