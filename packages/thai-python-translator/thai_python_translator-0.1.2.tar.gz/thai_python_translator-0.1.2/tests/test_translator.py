# tests/test_translator.py
import unittest
from translator.core import ThaiPythonTranslator, execute_translated_code
from io import StringIO
import sys

class TestThaiPythonTranslator(unittest.TestCase):
    def setUp(self):
        self.translator = ThaiPythonTranslator()
    
    def test_basic_translation(self):
        """Test basic function and print statement translation."""
        thai_code = """
ฟังก์ชัน ทักทาย():
    พิมพ์("สวัสดี")
"""
        expected = """
def ทักทาย():
    พิมพ์("สวัสดี")
"""
        translated, error = self.translator.translate(thai_code)
        self.assertIsNone(error)
        self.assertEqual(translated.strip(), expected.strip())
    
    def test_control_flow_translation(self):
        """Test if/else translation."""
        thai_code = """
ถ้า จริง:
    พิมพ์("จริง")
ทำอีก:
    พิมพ์("เท็จ")
"""
        expected = """
if True:
    พิมพ์("จริง")
else:
    พิมพ์("เท็จ")
"""
        translated, error = self.translator.translate(thai_code)
        self.assertIsNone(error)
        self.assertEqual(translated.strip(), expected.strip())

    def test_operators_translation(self):
        """Test operator translation."""
        thai_code = "ก = 1 บวก 2 คูณ 3"
        expected = "ก = 1 + 2 * 3"
        translated, error = self.translator.translate(thai_code)
        self.assertIsNone(error)
        self.assertEqual(translated.strip(), expected.strip())

    def test_string_preservation(self):
        """Test that string contents are not translated."""
        thai_code = 'พิมพ์("ฟังก์ชัน inside string should not translate")'
        expected = 'พิมพ์("ฟังก์ชัน inside string should not translate")'
        translated, error = self.translator.translate(thai_code)
        self.assertIsNone(error)
        self.assertEqual(translated.strip(), expected.strip())

    def test_syntax_error(self):
        """Test handling of syntax errors."""
        thai_code = "ฟังก์ชัน ):"  # Invalid syntax
        _, error = self.translator.translate(thai_code)
        self.assertIsNotNone(error)
        self.assertTrue("error" in error.lower())

class TestCodeExecution(unittest.TestCase):
    def setUp(self):
        """Set up string buffer to capture printed output."""
        self.held_output = StringIO()
        self.original_stdout = sys.stdout
        sys.stdout = self.held_output

    def tearDown(self):
        """Restore normal stdout."""
        sys.stdout = self.original_stdout

    def test_execute_hello_world(self):
        """Test executing a hello world program."""
        thai_code = """
ฟังก์ชัน ทักทาย():
    พิมพ์("สวัสดี โลก!")
ทักทาย()
"""
        execute_translated_code(thai_code)
        self.assertEqual(self.held_output.getvalue().strip(), "สวัสดี โลก!")

    def test_execute_math_operations(self):
        """Test executing mathematical operations."""
        thai_code = """
ก = 5
ข = 3
พิมพ์(ก บวก ข)
พิมพ์(ก คูณ ข)
"""
        execute_translated_code(thai_code)
        output = self.held_output.getvalue().strip().split('\n')
        self.assertEqual(output, ["8", "15"])

    def test_execute_error_handling(self):
        """Test error handling in code execution."""
        thai_code = """
พยายาม:
    พิมพ์(ไม่มีตัวแปรนี้)
จับข้อผิดพลาด:
    พิมพ์("จับข้อผิดพลาดได้")
"""
        execute_translated_code(thai_code)
        self.assertTrue("จับข้อผิดพลาดได้" in self.held_output.getvalue())