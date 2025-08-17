"""
API Authentication and Security Utilities
"""

import os
from functools import wraps
from flask import request, jsonify, current_app


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
            return jsonify({
                'error': 'API key required',
                'message': 'Please provide X-API-Key header'
            }), 401
        
        # Validate API key
        expected_api_key = current_app.config.get('API_KEY')
        if api_key != expected_api_key:
            return jsonify({
                'error': 'Invalid API key',
                'message': 'The provided API key is invalid'
            }), 401
        
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
                return jsonify({
                    'error': 'Invalid content type',
                    'message': 'Request must contain JSON data'
                }), 400
            
            data = request.get_json()
            
            # Check if JSON is valid
            if data is None:
                return jsonify({
                    'error': 'Invalid JSON',
                    'message': 'Request contains invalid JSON'
                }), 400
            
            # Validate required fields
            if required_fields:
                missing_fields = [field for field in required_fields if field not in data]
                if missing_fields:
                    return jsonify({
                        'error': 'Missing required fields',
                        'message': f'The following fields are required: {", ".join(missing_fields)}'
                    }), 400
            
            return f(*args, **kwargs)
        
        return decorated_function
    return decorator
