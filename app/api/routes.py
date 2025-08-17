"""
API Routes Blueprint
"""

from flask import Blueprint, request, jsonify
from app.utils.auth import require_api_key, validate_json_payload
from app.utils.helpers import success_response, error_response
from app.services.example_service import ExampleService

# Create API blueprint
api_bp = Blueprint('api', __name__, url_prefix='/api/v1')


@api_bp.route('/status', methods=['GET'])
def api_status():
    print("API status requested")
    
    """
    Get API status
    
    Returns:
        JSON response with API status information
    """
    return success_response({
        'api_version': 'v1',
        'status': 'running',
        'endpoints': {
            'status': 'GET /api/v1/status',
            'example': 'GET /api/v1/example',
            'example_post': 'POST /api/v1/example'
        }
    })


@api_bp.route('/example', methods=['GET'])
@require_api_key
def get_example():
    """
    Example GET endpoint with API key authentication
    
    Returns:
        JSON response with example data
    """
    try:
        example_service = ExampleService()
        data = example_service.get_example_data()
        return success_response(data, "Example data retrieved successfully")
    except Exception as e:
        return error_response(f"Failed to get example data: {str(e)}", 500)


@api_bp.route('/example', methods=['POST'])
@require_api_key
@validate_json_payload(['name', 'value'])
def create_example():
    """
    Example POST endpoint with API key authentication and JSON validation
    
    Expected JSON payload:
    {
        "name": "string",
        "value": "string",
        "description": "string (optional)"
    }
    
    Returns:
        JSON response with created example data
    """
    try:
        data = request.get_json()
        example_service = ExampleService()
        result = example_service.create_example(data)
        return success_response(result, "Example created successfully", 201)
    except Exception as e:
        return error_response(f"Failed to create example: {str(e)}", 500)


@api_bp.route('/example/<example_id>', methods=['GET'])
@require_api_key
def get_example_by_id(example_id):
    """
    Get example by ID
    
    Args:
        example_id: ID of the example to retrieve
        
    Returns:
        JSON response with example data
    """
    try:
        example_service = ExampleService()
        data = example_service.get_example_by_id(example_id)
        if not data:
            return error_response("Example not found", 404)
        return success_response(data, "Example retrieved successfully")
    except Exception as e:
        return error_response(f"Failed to get example: {str(e)}", 500)


@api_bp.route('/example/<example_id>', methods=['PUT'])
@require_api_key
@validate_json_payload(['name'])
def update_example(example_id):
    """
    Update example by ID
    
    Args:
        example_id: ID of the example to update
        
    Expected JSON payload:
    {
        "name": "string",
        "value": "string (optional)",
        "description": "string (optional)"
    }
    
    Returns:
        JSON response with updated example data
    """
    try:
        data = request.get_json()
        example_service = ExampleService()
        result = example_service.update_example(example_id, data)
        if not result:
            return error_response("Example not found", 404)
        return success_response(result, "Example updated successfully")
    except Exception as e:
        return error_response(f"Failed to update example: {str(e)}", 500)


@api_bp.route('/example/<example_id>', methods=['DELETE'])
@require_api_key
def delete_example(example_id):
    """
    Delete example by ID
    
    Args:
        example_id: ID of the example to delete
        
    Returns:
        JSON response confirming deletion
    """
    try:
        example_service = ExampleService()
        success = example_service.delete_example(example_id)
        if not success:
            return error_response("Example not found", 404)
        return success_response(message="Example deleted successfully")
    except Exception as e:
        return error_response(f"Failed to delete example: {str(e)}", 500)
