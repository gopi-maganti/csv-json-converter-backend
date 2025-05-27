import sys
import os
import pytest
from flask import Flask

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import create_app

# ---------------------- POSITIVE TEST CASES ----------------------

def test_app_creation() -> None:
    app = create_app()
    assert isinstance(app, Flask)
    assert app.config['UPLOAD_FOLDER'] == 'uploads'
    assert app.config['OUTPUT_FOLDER'] == 'converted'
    assert 'SWAGGER' in app.config

def test_registered_routes() -> None:
    app = create_app()
    client = app.test_client()
    response = client.post('/api/convert')  # Send minimal request
    assert response.status_code in (400, 405)
