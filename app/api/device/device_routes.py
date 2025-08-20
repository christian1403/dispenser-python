"""
Device API Routes Blueprint
"""

from flask import Blueprint, request, jsonify
from app.utils.auth import require_api_key, validate_json_payload
from app.utils.helpers import success_response, error_response
from app.services.device_service import DeviceService

# Create Device API blueprint
device_bp = Blueprint('device', __name__, url_prefix='/api/v1')


@device_bp.route('/devices', methods=['GET'])
@require_api_key
def get_devices():
    """
    Get all devices
    
    Query Parameters:
        page (int): Page number for pagination (default: 1)
        per_page (int): Items per page (default: 10)
        status (str): Filter by device status (optional)
    
    Returns:
        JSON response with list of devices
    """
    try:
        # Get query parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        status_filter = request.args.get('status', None, type=str)
        
        device_service = DeviceService()
        
        # If no pagination parameters, return all devices
        if page == 1 and per_page == 10 and not request.args.get('page') and not request.args.get('per_page'):
            data = device_service.get_all_devices()
        else:
            data = device_service.list_devices(page=page, per_page=per_page, status_filter=status_filter)
        
        return success_response(data, "Devices retrieved successfully")
    except Exception as e:
        return error_response(f"Failed to get devices: {str(e)}", 500)


@device_bp.route('/device', methods=['POST'])
@require_api_key
@validate_json_payload(['device_id', 'name'])
def create_device():
    """
    Create a new device
    
    Expected JSON payload:
    {
        "device_id": "string",
        "name": "string",
    }
    
    Returns:
        JSON response with created device data
    """
    try:
        data = request.get_json()
        device_service = DeviceService()
        result = device_service.create_device(data)
        return success_response(result, "Device created successfully", 201)
    except ValueError as ve:
        return error_response(str(ve), 400)
    except Exception as e:
        return error_response(f"Failed to create device: {str(e)}", 500)


@device_bp.route('/device/<device_id>', methods=['GET'])
@require_api_key
def get_device_by_id(device_id):
    """
    Get device by ID
    
    Args:
        device_id: ID of the device to retrieve
        
    Returns:
        JSON response with device data
    """
    try:
        device_service = DeviceService()
        data = device_service.get_device_by_id(device_id)
        if not data:
            return error_response("Device not found", 404)
        return success_response(data, "Device retrieved successfully")
    except Exception as e:
        return error_response(f"Failed to get device: {str(e)}", 500)


@device_bp.route('/device/<device_id>', methods=['PUT'])
@require_api_key
@validate_json_payload(['name'])
def update_device(device_id):
    """
    Update device by ID
    
    Args:
        device_id: ID of the device to update
        
    Expected JSON payload:
    {
        "name": "string",
        "sensors" : "list",
        "tools" : "list"
    }
    
    Returns:
        JSON response with updated device data
    """
    try:
        data = request.get_json()
        device_service = DeviceService()
        result = device_service.update_device(device_id, data)
        if not result:
            return error_response("Device not found", 404)
        return success_response(result, "Device updated successfully")
    except ValueError as ve:
        return error_response(str(ve), 400)
    except Exception as e:
        return error_response(f"Failed to update device: {str(e)}", 500)


@device_bp.route('/device/<device_id>', methods=['DELETE'])
@require_api_key
def delete_device(device_id):
    """
    Delete device by ID
    
    Args:
        device_id: ID of the device to delete
        
    Returns:
        JSON response confirming deletion
    """
    try:
        device_service = DeviceService()
        success = device_service.delete_device(device_id)
        if not success:
            return error_response("Device not found", 404)
        return success_response(success, message="Device deleted successfully")
    except Exception as e:
        return error_response(f"Failed to delete device: {str(e)}", 500)
