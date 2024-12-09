# translator/core.py
"""
Core translation functionality for Thai Python Translator.

This module provides the main translation logic for converting Thai Python code
to standard Python code. It handles keyword translation, operator conversion,
and code execution while preserving string literals and providing proper error handling.
"""

import re
import ast
import builtins
from typing import Tuple, Optional
from .keywords import KEYWORD_MAP, OPERATOR_MAP

class ThaiPythonTranslator:
    """
    Main translator class for converting Thai Python syntax to standard Python.

    This class handles the translation of Thai keywords and operators to their Python
    equivalents while preserving string literals and maintaining proper syntax.

    Attributes:
        sorted_keywords: List of Thai-to-Python keyword mappings, sorted by length
        sorted_operators: List of Thai-to-Python operator mappings, sorted by length
    """

    def __init__(self):
        """Initialize the translator with sorted keyword and operator mappings."""
        self._build_translation_patterns()
    
    def _build_translation_patterns(self):
        """
        Build sorted translation patterns for keywords and operators.
        
        Sorts keywords and operators by length (longest first) to prevent partial matches
        during translation. For example, 'มากกว่าเท่ากับ' should be translated before 'มากกว่า'.
        """
        self.sorted_keywords = sorted(
            KEYWORD_MAP.items(),
            key=lambda x: len(x[0]),
            reverse=True
        )
        self.sorted_operators = sorted(
            OPERATOR_MAP.items(),
            key=lambda x: len(x[0]),
            reverse=True
        )
    
    def translate(self, code: str) -> Tuple[str, Optional[str]]:
        """
        Translate Thai Python code to standard Python.

        Args:
            code: String containing Thai Python code

        Returns:
            A tuple containing:
            - The translated Python code (str)
            - An error message if translation failed (str or None)

        Example:
            >>> translator = ThaiPythonTranslator()
            >>> code = '''
            ... ฟังก์ชัน ทักทาย():
            ...     พิมพ์("สวัสดี!")
            ... '''
            >>> translated, error = translator.translate(code)
            >>> print(translated)
            def ทักทาย():
                print("สวัสดี!")
        """
        try:
            strings = {}
            code = self._preserve_strings(code, strings)
            
            for thai, python in self.sorted_keywords:
                code = re.sub(rf'\b{thai}\b', python, code)
            
            for thai, python in self.sorted_operators:
                code = code.replace(thai, python)
            
            code = self._restore_strings(code, strings)
            
            ast.parse(code)  # Validate syntax
            
            return code, None
        except Exception as e:
            return code, f"Translation error: {str(e)}"

    def _preserve_strings(self, code: str, strings: dict) -> str:
        """
        Preserve string literals during translation by replacing them with placeholders.

        Args:
            code: The source code containing string literals
            strings: Dictionary to store the mapping of placeholders to original strings

        Returns:
            Code with string literals replaced by placeholders
        """
        pattern = r'(["\'])((?:(?!\1).|\n)*?)\1'
        def replace(match):
            placeholder = f"__STR_{len(strings)}__"
            strings[placeholder] = match.group(0)
            return placeholder
        return re.sub(pattern, replace, code)
    
    def _restore_strings(self, code: str, strings: dict) -> str:
        """
        Restore preserved string literals by replacing placeholders.

        Args:
            code: The code with string placeholders
            strings: Dictionary mapping placeholders to original strings

        Returns:
            Code with original string literals restored
        """
        for placeholder, string in strings.items():
            code = code.replace(placeholder, string)
        return code

def execute_translated_code(thai_code: str):
    """
    Execute Thai Python code by translating it to standard Python and running it.

    This function handles the full process of translating and executing Thai Python code,
    including setting up the proper execution environment with Thai function names.

    Args:
        thai_code: String containing Thai Python code to execute

    Example:
        >>> thai_code = '''
        ... ฟังก์ชัน ทักทาย():
        ...     พิมพ์("สวัสดี!")
        ... ทักทาย()
        ... '''
        >>> execute_translated_code(thai_code)
        สวัสดี!
    """
    translator = ThaiPythonTranslator()
    python_code, error = translator.translate(thai_code)
    
    if error:
        print(f"Translation error: {error}")
        return

    try:
        globals_dict = {}
        
        # Add all Python builtins
        for name in dir(builtins):
            globals_dict[name] = getattr(builtins, name)
        
        # Add Thai function names
        globals_dict['พิมพ์'] = print
        globals_dict['ตัวเลข'] = int
        globals_dict['ทศนิยม'] = float
        globals_dict['ข้อความ'] = str
        globals_dict['รายการ'] = list
        globals_dict['พจนานุกรม'] = dict
        globals_dict['เซต'] = set
        
        exec(python_code, globals_dict)
    except Exception as e:
        from .runtime import translate_error
        translated_error = translate_error(e)
        print(f"Runtime error: {translated_error}")