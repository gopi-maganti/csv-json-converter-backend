import json
import os
import sys
import pytest

# Add the parent directory (project root) to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from typing import List, Dict, Any
from app.utils import read_csv, write_json, read_json, write_csv

# Sample data
sample_data: List[Dict[str, Any]] = [
    {
        "Customer Id": "CUST001",
        "First Name": "John",
        "Last Name": "Doe",
        "Company": "Acme Corp",
        "City": "New York",
        "Country": "USA",
        "Phone 1": "+1-555-1234",
        "Phone 2": "+1-555-5678",
        "Email": "john.doe@example.com",
        "Subscription Date": "2023-05-10",
        "Website": "https://www.acmecorp.com",
    },
    {
        "Customer Id": "CUST002",
        "First Name": "Jane",
        "Last Name": "Smith",
        "Company": "Globex Inc",
        "City": "Los Angeles",
        "Country": "USA",
        "Phone 1": "+1-555-9876",
        "Phone 2": "+1-555-4321",
        "Email": "jane.smith@globex.com",
        "Subscription Date": "2024-08-22",
        "Website": "https://www.globex.com",
    },
]

CSV_PATH = "test_sample.csv"
JSON_PATH = "test_sample.json"


@pytest.fixture(autouse=True)
def cleanup_files():
    """Fixture to clean up test files before and after test execution."""
    yield
    for path in [CSV_PATH, JSON_PATH, "roundtrip.csv"]:
        if os.path.exists(path):
            os.remove(path)


# ---------------------- POSITIVE TEST CASES ----------------------


def test_write_csv_and_read_csv() -> None:
    """Test writing to a CSV and reading it back."""
    write_csv(sample_data, CSV_PATH)
    read_data = read_csv(CSV_PATH)
    assert read_data == sample_data


def test_write_json_and_read_json() -> None:
    """Test writing to a JSON and reading it back."""
    write_json(sample_data, JSON_PATH)
    read_data = read_json(JSON_PATH)
    assert read_data == sample_data


def test_round_trip_csv_json_conversion() -> None:
    """Test complete round-trip: CSV -> JSON -> CSV."""
    write_csv(sample_data, CSV_PATH)
    data_from_csv = read_csv(CSV_PATH)
    write_json(data_from_csv, JSON_PATH)
    data_from_json = read_json(JSON_PATH)
    write_csv(data_from_json, "roundtrip.csv")
    final_data = read_csv("roundtrip.csv")
    assert final_data == sample_data


# ---------------------- NEGATIVE TEST CASES ----------------------


def test_read_csv_file_not_found() -> None:
    """Test reading a non-existent CSV file raises FileNotFoundError."""
    with pytest.raises(FileNotFoundError):
        read_csv("nonexistent.csv")


def test_read_json_file_not_found() -> None:
    """Test reading a non-existent JSON file raises FileNotFoundError."""
    with pytest.raises(FileNotFoundError):
        read_json("nonexistent.json")


def test_write_csv_with_empty_data() -> None:
    """Test writing an empty list to CSV should not create a file."""
    write_csv([], CSV_PATH)
    assert not os.path.exists(CSV_PATH)


def test_write_json_with_empty_data() -> None:
    """Test writing an empty list to JSON creates valid empty JSON array."""
    write_json([], JSON_PATH)
    with open(JSON_PATH, "r", encoding="utf-8") as file:
        assert file.read().strip() == "[]"


def test_read_json_invalid_format() -> None:
    """Test reading a malformed JSON file raises JSONDecodeError."""
    with open(JSON_PATH, "w", encoding="utf-8") as file:
        file.write("INVALID JSON")
    with pytest.raises(json.JSONDecodeError):
        read_json(JSON_PATH)


def test_write_csv_with_inconsistent_keys() -> None:
    """Test writing CSV with rows having different keys (inconsistent keys)."""
    inconsistent_data = [
        {"name": "Alice", "age": "30"},
        {"name": "Bob", "Company": "Globex Inc"},
    ]
    # Option 1: ignore extra keys (ensure this is handled in utils.write_csv)
    write_csv(inconsistent_data, CSV_PATH)
    read_data = read_csv(CSV_PATH)
    assert len(read_data) == 2
    assert "name" in read_data[0]
