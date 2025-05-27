import os
import json
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.services.converter import convert_csv_to_json, convert_json_to_csv

sample_data = [
    {"name": "Alice", "age": "30"},
    {"name": "Bob", "age": "25"}
]

@pytest.fixture(autouse=True)
def cleanup_files():
    yield
    for path in ["sample.csv", "output.json", "input.json", "output.csv"]:
        if os.path.exists(path):
            os.remove(path)

# ---------------------- POSITIVE TEST CASES ----------------------

def test_convert_csv_to_json() -> None:
    with open("sample.csv", "w", encoding="utf-8") as f:
        f.write("name,age\nAlice,30\nBob,25\n")

    convert_csv_to_json("sample.csv", "output.json")
    assert os.path.exists("output.json")

    with open("output.json", encoding="utf-8") as f:
        content = json.load(f)
    assert content == sample_data

def test_convert_json_to_csv() -> None:
    with open("input.json", "w", encoding="utf-8") as f:
        json.dump(sample_data, f)

    convert_json_to_csv("input.json", "output.csv")
    assert os.path.exists("output.csv")

    with open("output.csv", encoding="utf-8") as f:
        content = f.read()
    assert "name,age" in content and "Alice" in content

# ---------------------- NEGATIVE TEST CASES ----------------------

def test_convert_invalid_csv_path() -> None:
    with pytest.raises(FileNotFoundError):
        convert_csv_to_json("nonexistent.csv", "out.json")

def test_convert_invalid_json_path() -> None:
    with pytest.raises(FileNotFoundError):
        convert_json_to_csv("nonexistent.json", "out.csv")
