import unittest
from translator.keywords import KEYWORD_MAP, OPERATOR_MAP

class TestKeywordMaps(unittest.TestCase):
    def test_keyword_completeness(self):
        """Test that essential keywords are present."""
        essential_keywords = {
            "ฟังก์ชัน": "def",
            "ถ้า": "if",
            "ทำอีก": "else",
            "พิมพ์": "print"
        }
        for thai, python in essential_keywords.items():
            self.assertIn(thai, KEYWORD_MAP)
            self.assertEqual(KEYWORD_MAP[thai], python)
    
    def test_operator_completeness(self):
        """Test that essential operators are present."""
        essential_operators = {
            "บวก": "+",
            "ลบ": "-",
            "คูณ": "*",
            "หาร": "/"
        }
        for thai, python in essential_operators.items():
            self.assertIn(thai, OPERATOR_MAP)
            self.assertEqual(OPERATOR_MAP[thai], python)