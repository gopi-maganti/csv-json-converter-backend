import os
import json
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.services.file_conversion import perform_conversion

sample_data = [
    {"id": 1, "name": "Alice"},
    {"id": 2, "name": "Bob"}
]

@pytest.fixture(autouse=True)
def cleanup_files():
    yield
    for f in ["sample.csv", "sample.json", "converted/sample.json", "converted/sample.csv"]:
        if os.path.exists(f):
            os.remove(f)
    if os.path.exists("converted"):
        os.rmdir("converted")

# ---------------------- POSITIVE TEST CASES ----------------------

def test_perform_csv_to_json() -> None:
    os.makedirs("converted", exist_ok=True)
    with open("sample.csv", "w") as f:
        f.write("id,name\n1,Alice\n2,Bob\n")

    result = perform_conversion("sample.csv", "converted", "json")
    assert os.path.exists(os.path.join("converted", result))

def test_perform_json_to_csv() -> None:
    os.makedirs("converted", exist_ok=True)
    with open("sample.json", "w") as f:
        json.dump(sample_data, f)

    result = perform_conversion("sample.json", "converted", "csv")
    assert os.path.exists(os.path.join("converted", result))

# ---------------------- NEGATIVE TEST CASES ----------------------

def test_perform_invalid_file_type() -> None:
    with open("invalid.txt", "w") as f:
        f.write("unsupported content")

    with pytest.raises(ValueError):
        perform_conversion("invalid.txt", ".", "csv")

    os.remove("invalid.txt")