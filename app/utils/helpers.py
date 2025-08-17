"""
Utility functions for the Flask API
"""

import json
import uuid
from datetime import datetime
from flask import jsonify


def generate_uuid():
    """Generate a unique UUID string"""
    return str(uuid.uuid4())


def current_timestamp():
    """Get current timestamp in ISO format"""
    return datetime.utcnow().isoformat() + 'Z'


def success_response(data=None, message="Success", status_code=200):
    """
    Create a standardized success response
    
    Args:
        data: Response data
        message: Success message
        status_code: HTTP status code
        
    Returns:
        Flask response object
    """
    response = {
        'success': True,
        'message': message,
        'timestamp': current_timestamp()
    }
    
    if data is not None:
        response['data'] = data
    
    return jsonify(response), status_code


def error_response(message="An error occurred", status_code=400, error_code=None):
    """
    Create a standardized error response
    
    Args:
        message: Error message
        status_code: HTTP status code
        error_code: Custom error code
        
    Returns:
        Flask response object
    """
    response = {
        'success': False,
        'error': message,
        'timestamp': current_timestamp()
    }
    
    if error_code:
        response['error_code'] = error_code
    
    return jsonify(response), status_code


def paginate_response(items, page, per_page, total):
    """
    Create a paginated response
    
    Args:
        items: List of items for current page
        page: Current page number
        per_page: Items per page
        total: Total number of items
        
    Returns:
        Dict with paginated data
    """
    return {
        'items': items,
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': total,
            'pages': (total + per_page - 1) // per_page,
            'has_next': page * per_page < total,
            'has_prev': page > 1
        }
    }
