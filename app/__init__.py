"""
Flask Application Factory
"""

import os
from flask import Flask
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from app.api.routes import api_bp
from app.utils.config import Config
from app.utils.error_handlers import error_handlers


def create_app(config_class=Config):
    """
    Create and configure Flask application
    
    Args:
        config_class: Configuration class to use
        
    Returns:
        Flask: Configured Flask application instance
    """
    # Create Flask app
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config_class)
    
    # Initialize CORS
    CORS(app, origins=app.config.get('CORS_ORIGINS', '*'))
    
    # Initialize rate limiter
    limiter = Limiter(
        key_func=get_remote_address,
        default_limits=[f"{app.config.get('RATE_LIMIT_PER_MINUTE', 60)} per minute"]
    )
    limiter.init_app(app)
    
    # Register blueprints
    app.register_blueprint(api_bp, url_prefix=f"/api/{app.config.get('API_VERSION', 'v1')}")
    
    # Register error handlers
    error_handlers(app)
    
    # Health check endpoint
    @app.route('/health')
    def health_check():
        return {'status': 'healthy', 'message': 'API is running'}, 200
    
    return app
