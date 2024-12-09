import unittest
from translator.runtime import translate_error, ERROR_MAP

class TestRuntimeTranslation(unittest.TestCase):
    def test_error_translation(self):
        """Test translation of common Python errors."""
        # Test NameError translation
        error = NameError("name 'x' is not defined")
        translated = translate_error(error)
        self.assertEqual(translated, ERROR_MAP["NameError"])
        
        # Test TypeError translation
        error = TypeError("unsupported operand type(s)")
        translated = translate_error(error)
        self.assertEqual(translated, ERROR_MAP["TypeError"])
    
    def test_unknown_error(self):
        """Test handling of unknown error types."""
        class CustomError(Exception):
            pass
        
        error = CustomError("custom error")
        translated = translate_error(error)
        self.assertEqual(translated, str(error))
