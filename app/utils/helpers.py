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
    Create a standardized success response.

    Args:
        data (any, optional): Response data. Defaults to None.
        message (str, optional): Success message. Defaults to "Success".
        status_code (int, optional): HTTP status code. Defaults to 200.

    Returns:
        tuple: Flask response object (jsonify, status_code)
    """
    response = {
        'status': 'success',
        'message': message,
        'result': {
            'data': data if data is not None else []
        },
        'timestamp': current_timestamp()
    }
    
    return jsonify(response), status_code


def error_response(message="An error occurred", status_code=400, error_code=None):
    """
    Create a standardized error response.

    Args:
        message (str, optional): Error message. Defaults to "An error occurred".
        status_code (int, optional): HTTP status code. Defaults to 400.
        error_code (str|int, optional): Custom error code. Defaults to None.

    Returns:
        tuple: Flask response object (jsonify, status_code)
    """
    response = {
        'status': 'error',
        'message': message,
        'result': {},
        'timestamp': current_timestamp()
    }
    
    if error_code:
        response['error_code'] = error_code
    
    return jsonify(response), status_code


def paginate_response(data=None, page=1, per_page=10, total=0, message="Success", status_code=200):
    """
    Create a standardized paginated response.

    Args:
        data (list|None, optional): List of items for current page. Defaults to [] if None.
        page (int, optional): Current page number. Defaults to 1.
        per_page (int, optional): Number of items per page. Defaults to 10.
        total (int, optional): Total number of items. Defaults to 0.
        message (str, optional): Response message. Defaults to "Success".
        status_code (int, optional): HTTP status code. Defaults to 200.

    Returns:
        tuple: Flask response object (jsonify, status_code)
    """
    response = {
        'status': 'success',
        'message': message,
        'result': {
            'data': data if data is not None else [],  # fallback ke list kosong
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': total,
                'pages': (total + per_page - 1) // per_page if per_page > 0 else 0,
                'has_next': page * per_page < total,
                'has_prev': page > 1
            }
        },
        'timestamp': current_timestamp()
    }
    
    return jsonify(response), status_code

