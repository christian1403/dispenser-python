"""
Configuration for pytest
"""

import pytest
import os
import sys

# Add the app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app import create_app
from app.utils.config import TestingConfig


@pytest.fixture
def app():
    """Create and configure a test app"""
    app = create_app(TestingConfig)
    return app


@pytest.fixture
def client(app):
    """Create a test client"""
    return app.test_client()


@pytest.fixture
def api_headers():
    """Headers with API key for authenticated requests"""
    return {
        'Content-Type': 'application/json',
        'X-API-Key': 'test-api-key'
    }
