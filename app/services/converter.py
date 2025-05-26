from app.utils import read_csv, write_json, read_json, write_csv


def convert_csv_to_json(csv_file_path: str, json_file_path: str) -> None:
    """
    Converts a CSV file to a JSON file.

    Args:
        csv_file_path (str): Path to the input CSV file.
        json_file_path (str): Path to the output JSON file.
    """
    data = read_csv(csv_file_path)
    write_json(data, json_file_path)
    print(f"Converted {csv_file_path} to {json_file_path}")


def convert_json_to_csv(json_file_path: str, csv_file_path: str) -> None:
    """
    Converts a JSON file to a CSV file.

    Args:
        json_file_path (str): Path to the input JSON file.
        csv_file_path (str): Path to the output CSV file.
    """
    data = read_json(json_file_path)
    write_csv(data, csv_file_path)
    print(f"Converted {json_file_path} to {csv_file_path}")
