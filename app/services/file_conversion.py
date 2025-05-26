import os
from app.services.converter import convert_csv_to_json, convert_json_to_csv


def perform_conversion(upload_path: str, output_folder: str, target_format: str) -> str:
    """
    Perform file conversion based on the target format.
    Args:
        upload_path (str): Path to the uploaded file.
        output_folder (str): Directory where the converted file will be saved.
        target_format (str): Target format for conversion ('csv' or 'json').
    Returns:
        str: The name of the converted file.
    """
    base_filename = os.path.splitext(os.path.basename(upload_path))[0]

    if upload_path.endswith(".csv") and target_format == "json":
        output_path = os.path.join(output_folder, f"{base_filename}.json")
        convert_csv_to_json(upload_path, output_path)
    elif upload_path.endswith(".json") and target_format == "csv":
        output_path = os.path.join(output_folder, f"{base_filename}.csv")
        convert_json_to_csv(upload_path, output_path)
    else:
        raise ValueError("Unsupported file format or conversion type.")

    return os.path.basename(output_path)
