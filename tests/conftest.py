import sys
from pathlib import Path

# Add parent directory to path so we can import app and models
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from app import create_app, db
from models import User, Post


@pytest.fixture
def app():
    """Create application for testing."""
    test_config = {
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
    }
    app = create_app(test_config)
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Test client for the app."""
    return app.test_client()