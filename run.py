from app import create_app
from app.utils import ensure_directories

app = create_app()

"""
Main entry point for the Flask application.
This function ensures that the necessary directories exist
"""

if __name__ == "__main__":
    ensure_directories([app.config["UPLOAD_FOLDER"], app.config["OUTPUT_FOLDER"]])
    app.run(debug=True)
