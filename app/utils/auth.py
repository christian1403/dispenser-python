"""
API Authentication and Security Utilities
"""

import os
from functools import wraps
from flask import request, current_app, abort

def require_api_key(f):
    """
    Decorator to require API key authentication
    
    Args:
        f: Function to decorate
        
    Returns:
        Decorated function that requires API key
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Get API key from headers
        api_key = request.headers.get('X-API-Key')
        
        # Check if API key is provided
        if not api_key:
            abort(403, description='API key is missing')
        
        # Validate API key
        expected_api_key = current_app.config.get('API_KEY')
        if api_key != expected_api_key:
            abort(401, description='Invalid API key')
        
        return f(*args, **kwargs)
    
    return decorated_function


def validate_json_payload(required_fields=None):
    """
    Decorator to validate JSON payload
    
    Args:
        required_fields: List of required fields in JSON payload
        
    Returns:
        Decorator function
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Check if request contains JSON
            if not request.is_json:
                abort(400, description='Request must contain JSON data')
            
            data = request.get_json(silent=True)
            
            # Check if JSON is valid
            if data is None:
                abort(400, description='Request contains invalid JSON')
            
            # Validate required fields
            if required_fields:
                missing_fields = [field for field in required_fields if field not in data]
                if missing_fields:
                    abort(
                        400, 
                        description=f'The following fields are required: {", ".join(missing_fields)}'
                    )
            
            return f(*args, **kwargs)
        
        return decorated_function
    return decorator
