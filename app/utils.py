import os
import csv
import json
from typing import List, Dict, Any


def read_csv(file_path: str) -> List[Dict[str, Any]]:
    """
    Reads a CSV file and returns a list of dictionaries.
    Each dictionary represents a row in the CSV file.
    """
    with open(file_path, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        data = [row for row in reader]
    return data


def write_json(data: List[Dict[str, Any]], file_path: str) -> None:
    """
    Writes a list of dictionaries to a JSON file.
    Each dictionary represents a row in the CSV file.
    """
    with open(file_path, mode="w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


def read_json(file_path: str) -> List[Dict[str, Any]]:
    """
    Reads a JSON file and returns a list of dictionaries.
    Each dictionary represents a row in the CSV file.
    """
    with open(file_path, mode="r", encoding="utf-8") as file:
        data = json.load(file)
    return data


def write_csv(data: List[Dict[str, Any]], file_path: str) -> None:
    """
    Writes a list of dictionaries to a CSV file.
    Each dictionary represents a row in the CSV file.
    """
    if not data:
        return
    with open(file_path, mode="w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys(), extrasaction="ignore")
        writer.writeheader()
        writer.writerows(data)


def allowed_file(filename: str, allowed_extensions: set) -> bool:
    """
    Check if the file has an allowed extension.
    """
    return "." in filename and filename.rsplit(".", 1)[1].lower() in allowed_extensions


def ensure_directories(paths: List[str]) -> None:
    """
    Ensure that the specified directories exist.
    If they do not exist, create them.
    """
    for path in paths:
        os.makedirs(path, exist_ok=True)
