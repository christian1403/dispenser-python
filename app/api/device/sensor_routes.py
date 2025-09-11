"""
Device API Routes Blueprint
"""

from flask import Blueprint, request, jsonify
from app.utils.auth import require_api_key, validate_json_payload
from app.utils.helpers import success_response, error_response
from app.services.sensor_service import SensorService

# Create Device API blueprint
sensor_bp = Blueprint('sensor', __name__, url_prefix='/api/v1')

@sensor_bp.route('/device/<device_id>/sensors', methods=['GET'])
@require_api_key
def get_sensors(device_id):
    """
    Get all sensors for a specific device

    Query Parameters:
        page (int): Page number for pagination (default: 1)
        per_page (int): Items per page (default: 10)
        status (str): Filter by device status (optional)
    
    Returns:
        JSON response with list of sensors
    """
    try:
        # Get query parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        status_filter = request.args.get('status', None, type=str)

        sensor_service = SensorService()

        # If no pagination parameters, return all sensors
        if page == 1 and per_page == 10 and not request.args.get('page') and not request.args.get('per_page'):
            data = sensor_service.get_all_sensors(device_id)
        else:
            data = sensor_service.list_sensors(device_id, page=page, per_page=per_page, status_filter=status_filter)

        return success_response(data, "Sensors retrieved successfully")
    except ValueError as e:
        return error_response(f"Failed to get sensors: {str(e)}", 400)
    except Exception as e:
        return error_response(f"Failed to get sensors: {str(e)}", 500)


@sensor_bp.route('/device/<device_id>/sensor', methods=['POST'])
@require_api_key
@validate_json_payload(['value', 'unit', 'sensor_type'])
def create_sensor(device_id):
    """
    Create a new sensor for a specific device

    Expected JSON payload:
    {
        "value": 0.0,
        "unit": "string",
        "sensor_type": "string"
    }

    Returns:
        JSON response with created sensor data
    """
    try:
        data = request.get_json()
        sensor_service = SensorService()
        result = sensor_service.create_sensor(data, device_id)
        return success_response(result, "Sensor created successfully", 201)
    except ValueError as ve:
        return error_response(str(ve), 400)
    except Exception as e:
        return error_response(f"Failed to create sensor: {str(e)}", 500)

@sensor_bp.route('/device/<device_id>/sensor/<sensor_id>', methods=['GET'])
@require_api_key
def get_sensor_by_id(device_id, sensor_id):
    """
    Get sensor by ID

    Args:
        device_id: ID of the device to retrieve
        sensor_id: ID of the sensor to retrieve

    Returns:
        JSON response with sensor data
    """
    try:
        sensor_service = SensorService()
        data = sensor_service.get_sensor_by_id(device_id, sensor_id)
        if not data:
            return error_response("Sensor not found", 404)
        return success_response(data, "Sensor retrieved successfully")
    except Exception as e:
        return error_response(f"Failed to get sensor: {str(e)}", 500)

@sensor_bp.route('/device/<device_id>/sensor/<sensor_id>', methods=['DELETE'])
@require_api_key
def delete_sensor(device_id, sensor_id):
    """
    Delete sensor by ID

    Args:
        device_id: ID of the device
        sensor_id: ID of the sensor

    Returns:
        JSON response confirming deletion
    """
    try:
        sensor_service = SensorService()
        success = sensor_service.delete_sensor(device_id, sensor_id)
        if not success:
            return error_response("Sensor not found", 404)
        return success_response(success, message="Sensor deleted successfully")
    except ValueError as e:
        return error_response(f"Failed to delete sensor: {str(e)}", 400)
    except Exception as e:
        return error_response(f"Failed to delete sensor: {str(e)}", 500)