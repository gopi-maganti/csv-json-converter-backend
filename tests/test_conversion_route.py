import os
import io
import sys
import pytest
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['UPLOAD_FOLDER'] = 'uploads'
    app.config['OUTPUT_FOLDER'] = 'converted'
    with app.test_client() as client:
        yield client

@pytest.fixture(autouse=True)
def cleanup_dirs():
    yield
    for folder in ['uploads', 'converted']:
        if os.path.exists(folder):
            for file in os.listdir(folder):
                os.remove(os.path.join(folder, file))
            os.rmdir(folder)

# ---------------------- POSITIVE TEST CASES ----------------------

def test_valid_csv_to_json_conversion(client):
    os.makedirs('uploads', exist_ok=True)
    os.makedirs('converted', exist_ok=True)
    data = {
        'file': (io.BytesIO(b'name,age\nAlice,30\nBob,25'), 'test.csv'),
        'target': 'json'
    }
    response = client.post('/api/convert', data=data, content_type='multipart/form-data')
    assert response.status_code == 200
    response_data = response.get_json()
    assert 'output_file' in response_data
    assert response_data['output_file'].endswith('.json')

def test_valid_json_to_csv_conversion(client):
    os.makedirs('uploads', exist_ok=True)
    os.makedirs('converted', exist_ok=True)
    json_bytes = json.dumps([{"name": "Alice", "age": "30"}, {"name": "Bob", "age": "25"}]).encode()
    data = {
        'file': (io.BytesIO(json_bytes), 'test.json'),
        'target': 'csv'
    }
    response = client.post('/api/convert', data=data, content_type='multipart/form-data')
    assert response.status_code == 200
    response_data = response.get_json()
    assert 'output_file' in response_data
    assert response_data['output_file'].endswith('.csv')

# ---------------------- NEGATIVE TEST CASES ----------------------

def test_missing_file_field(client):
    response = client.post('/api/convert', data={'target': 'json'})
    assert response.status_code == 400
    assert 'error' in response.get_json()

def test_invalid_file_type(client):
    data = {
        'file': (io.BytesIO(b'invalid content'), 'test.txt'),
        'target': 'json'
    }
    response = client.post('/api/convert', data=data, content_type='multipart/form-data')
    assert response.status_code == 400
    assert 'error' in response.get_json()

def test_invalid_target_format(client):
    data = {
        'file': (io.BytesIO(b'name,age\nAlice,30'), 'test.csv'),
        'target': 'xml'
    }
    response = client.post('/api/convert', data=data, content_type='multipart/form-data')
    assert response.status_code == 400
    assert 'error' in response.get_json()
