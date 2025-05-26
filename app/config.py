import os


class Config:
    """
    Configuration class for the Flask application.
    This class contains settings for file upload and conversion.
    """

    UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads")
    OUTPUT_FOLDER = os.path.join(os.getcwd(), "converted")
    ALLOWED_EXTENSIONS = {"csv", "json"}
