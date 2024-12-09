# Thai Python Translator

A tool that allows you to write Python code using Thai syntax. Write Python programs in Thai while maintaining full Python compatibility!

## Features

- Write Python code using Thai keywords and syntax
- Built-in support for common Python functions in Thai
- Automatic translation to standard Python
- Thai error messages for better debugging
- Support for:
  - Functions (ฟังก์ชัน)
  - Control flow (ถ้า, ทำอีก, หรือถ้า)
  - Error handling (พยายาม, จับข้อผิดพลาด)
  - Basic operators (บวก, ลบ, คูณ, หาร)
  - Built-in functions (พิมพ์, ตัวเลข, ข้อความ, etc.)

## Installation

```bash
pip install thai-python-translator
```

## Usage

1. Create a Thai Python file (e.g., `hello.py`):
```python
ฟังก์ชัน ทักทาย():
    พิมพ์("สวัสดี โลก!")

ทักทาย()
```

2. Run it using the CLI:
```bash
thai-python hello.py
```

## Examples

### Hello World
```python
ฟังก์ชัน ทักทาย():
    ถ้า จริง:
        พิมพ์("สวัสดี โลก!")

ทักทาย()
```

### Grade Calculator
```python
ฟังก์ชัน คำนวณเกรด(คะแนน):
    ถ้า คะแนน มากกว่าเท่ากับ 80:
        ส่งคืน "A"
    หรือถ้า คะแนน มากกว่าเท่ากับ 70:
        ส่งคืน "B"
    หรือถ้า คะแนน มากกว่าเท่ากับ 60:
        ส่งคืน "C"
    ทำอีก:
        ส่งคืน "F"

พยายาม:
    คะแนน = ตัวเลข(input("ใส่คะแนนของคุณ: "))
    เกรด = คำนวณเกรด(คะแนน)
    พิมพ์(f"เกรดของคุณคือ: {เกรด}")
จับข้อผิดพลาด:
    พิมพ์("กรุณาใส่ตัวเลขที่ถูกต้อง")
```

## Publishing to PyPI

To publish this to PyPI:

1. Create accounts on PyPI and Test PyPI
2. Install build tools:
```bash
pip install build twine
```

3. Build the package:
```bash
python -m build
```

4. Upload to Test PyPI first:
```bash
twine upload --repository testpypi dist/*
```

5. Test the installation:
```bash
pip install --index-url https://test.pypi.org/simple/ thai-python-translator
```

6. If everything works, upload to real PyPI:
```bash
twine upload dist/*
```

## Development

To contribute to this project:

1. Clone the repository
2. Install in development mode:
```bash
pip install -e .
```

## TODO

Future enhancements could include:
- More Thai keywords and built-in functions
- Better error messages and debugging tools
- Support for more Python features (classes, decorators, etc.)
- Documentation in Thai
- Interactive REPL in Thai

## License

MIT