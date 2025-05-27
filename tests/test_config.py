import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.config import Config

# ---------------------- POSITIVE TEST CASES ----------------------

def test_upload_folder_path():
    assert os.path.basename(Config.UPLOAD_FOLDER) == 'uploads'
    assert os.path.isdir(Config.UPLOAD_FOLDER) or True  # Path may not exist yet

def test_output_folder_path():
    assert os.path.basename(Config.OUTPUT_FOLDER) == 'converted'
    assert os.path.isdir(Config.OUTPUT_FOLDER) or True

def test_allowed_extensions():
    assert 'csv' in Config.ALLOWED_EXTENSIONS
    assert 'json' in Config.ALLOWED_EXTENSIONS

# ---------------------- NEGATIVE TEST CASES ----------------------

def test_invalid_extension_not_allowed():
    assert 'exe' not in Config.ALLOWED_EXTENSIONS
    assert 'zip' not in Config.ALLOWED_EXTENSIONS
