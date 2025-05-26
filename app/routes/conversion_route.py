from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
import os

from app.services.file_conversion import perform_conversion
from app.utils import allowed_file
from flasgger import swag_from

bp = Blueprint("convert_routes", __name__, url_prefix="/api")


@bp.route("/convert", methods=["POST"])
@swag_from(
    {
        "tags": ["Conversion"],
        "consumes": ["multipart/form-data"],
        "parameters": [
            {
                "name": "file",
                "in": "formData",
                "type": "file",
                "required": True,
                "description": "CSV or JSON file to upload",
            },
            {
                "name": "target",
                "in": "formData",
                "type": "string",
                "enum": ["csv", "json"],
                "required": True,
                "description": "Target format to convert to",
            },
        ],
        "responses": {
            200: {
                "description": "Conversion successful",
                "examples": {
                    "application/json": {
                        "message": "Conversion successful",
                        "output_file": "converted_file.json",
                    }
                },
            },
            400: {"description": "Bad request"},
            500: {"description": "Server error"},
        },
    }
)
def convert_file():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]
    target_format = request.form.get("target")

    if not file or file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    if not target_format or target_format not in {"csv", "json"}:
        return jsonify({"error": "Invalid or missing target format"}), 400

    if allowed_file(file.filename, {"csv", "json"}):
        filename = secure_filename(file.filename)
        upload_path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
        file.save(upload_path)

        try:
            output_filename = perform_conversion(
                upload_path, current_app.config["OUTPUT_FOLDER"], target_format
            )
            return (
                jsonify(
                    {"message": "Conversion successful", "output_file": output_filename}
                ),
                200,
            )
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return jsonify({"error": "Invalid file type"}), 400
