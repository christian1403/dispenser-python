"""
Device Service for handling business logic
"""

import uuid
from datetime import datetime
from app.models.sensor_model import SensorModel
from app.utils.helpers import generate_uuid, current_timestamp
from app.utils.database import DatabaseMongo
from app.services.calibration_service import CalibrationService
from bson import ObjectId

dbSensors = DatabaseMongo.db.sensors
dbDevices = DatabaseMongo.db.devices
class SensorService:
    """Service class for handling sensor-related operations"""
    
    def __init__(self):
        """Initialize the service with calibration service"""
        self.calibration_service = CalibrationService()
    def get_all_sensors(self, device_id):
        """
        Get all sensor data for a specific device

        Args:
            device_id: ID of the device

        Returns:
            List of sensor data
        """

        check = dbDevices.find_one({"device_id" : device_id})
        if not check:
            raise ValueError("Device with this ID does not exist")

        docs = dbSensors.find({"device_id": device_id})
        if docs:
            sensors = [SensorModel.from_mongo(doc).dict() for doc in docs]
            return {"sensors": sensors}
        return []

    def create_sensor(self, data, device_id):
        """
        Create a new sensor

        Args:
            data: Dictionary containing sensor data
            
        Returns:
            Created sensor data
        """
        check = dbDevices.find_one({"device_id": device_id})
        
        if not check:
            raise ValueError("Device with this ID does not exist")

        existing_sensors = check.get("sensors", {})
        raw_value = data.get("value")
        sensor_type = data.get("sensor_type", "").lower()
        
        # Apply calibration based on sensor type
        calibrated_result = self._apply_calibration(sensor_type, raw_value)
        calibrated_value = calibrated_result.get('value', 0.0)
        calibrated_unit = calibrated_result.get('unit', data.get("unit", ""))
        
        sensor = {
            "device_id": device_id,
            "timestamp": current_timestamp(),
            "sensor_type": sensor_type,
            "value": calibrated_value,  # Use calibrated value
            "raw_value": raw_value,     # Store original raw value
            "unit": calibrated_unit,    # Use calibrated unit
            # "calibration_data": calibrated_result,  # Store full calibration info
            # "status": 1,
        }

        updateSensor = {
            sensor_type: {
                "value": calibrated_value,
                "raw_value": raw_value,
                "unit": calibrated_unit,
                "calibration_date": current_timestamp(),
                "calibration_data": calibrated_result,
                "status": True,
                "type": sensor_type
            }
        }

        merged = {**existing_sensors, **updateSensor}
        dbDevices.update_one({"device_id": device_id}, {"$set": {"sensors": merged}})
        result = dbSensors.insert_one(sensor)
        inserted_doc = dbSensors.find_one({"_id": result.inserted_id})
        return {"sensor": SensorModel.from_mongo(inserted_doc).dict()}
    
    def _apply_calibration(self, sensor_type, raw_value):
        """
        Apply calibration based on sensor type
        
        Args:
            sensor_type: Type of sensor (ph, tds, turbidity)
            raw_value: Raw sensor value
            
        Returns:
            Dictionary containing calibrated value and metadata
        """
        try:
            if sensor_type == "ph":
                return self.calibration_service.calibrate_ph(raw_value)
            elif sensor_type == "tds":
                return self.calibration_service.calibrate_tds(raw_value)
            elif sensor_type == "turbidity":
                return self.calibration_service.calibrate_turbidity(raw_value)
            else:
                # For unknown sensor types, return default values
                return {
                    'value': 0.0,
                    'unit': 'unknown',
                    'raw_value': raw_value,
                    'sensor_type': sensor_type,
                    'status': 'unsupported',
                    'calibration_timestamp': datetime.utcnow().isoformat()
                }
        except Exception as e:
            # If calibration fails, return error information
            return {
                'value': 0.0,
                'unit': 'error',
                'raw_value': raw_value,
                'sensor_type': sensor_type,
                'status': 'calibration_error',
                'error': str(e),
                'calibration_timestamp': datetime.utcnow().isoformat()
            } 
    
    def get_sensor_by_id(self, device_id, sensor_id):
        """
        Get sensor by ID
        
        Args:
            device_id: ID of the device
            sensor_id: ID of the sensor
        """
        check = dbDevices.find_one({"device_id": device_id})
        if not check:
            raise ValueError("Device with this ID does not exist")

        sensor = dbSensors.find_one({"_id": ObjectId(sensor_id), "device_id": device_id})
        if sensor:
            return {"sensor": SensorModel.from_mongo(sensor).dict()}
        return None

    def update_sensor(self, sensor_id, data):
        """
        Update sensor by ID

        Args:
            sensor_id: ID of the sensor
            data: Updated data
            
        Returns:
            Updated sensor data or None if not found
        """
        sensor = dbSensors.find_one({"_id": ObjectId(sensor_id)})
        if not sensor:
            return None

        sensor_data = SensorModel.from_mongo(sensor).dict()


        # Update fields
        update_data = {
            "value" : data.get("value", sensor_data['value']),
            "unit" : data.get("unit", sensor_data['unit']),
            "status" : data.get("status", sensor_data['status'])
        }

        dbSensors.update_one({"_id": ObjectId(sensor_id)}, {"$set": update_data})

        sensorUpdated = dbSensors.find_one({"_id": ObjectId(sensor_id)})
        return {"sensor": SensorModel.from_mongo(sensorUpdated).dict()}

    def delete_sensor(self, device_id, sensor_id):
        """
        Delete sensor by ID
        
        Args:
            device_id: ID of the device
            sensor_id: ID of the sensor
        """
        check = dbDevices.find_one({"device_id": device_id})
        if not check:
            raise ValueError("Device with this ID does not exist")

        sensor = dbSensors.find_one({"_id": ObjectId(sensor_id), "device_id": device_id})
        if not sensor:
            return False
        dbSensors.delete_one({"_id": ObjectId(sensor_id)})

        return {"sensor": SensorModel.from_mongo(sensor).dict()}

    def list_sensors(self, page=1, per_page=10, status_filter=None):
        """
        List sensors with pagination and optional status filter

        Args:
            page: Page number
            per_page: Items per page
            status_filter: Optional status filter

        Returns:
            Paginated list of sensors
        """
        sensors = list(self._storage.values())

        """
        Args:
            page: Page number
            per_page: Items per page
            status_filter: Optional status filter

        Returns:
            Paginated list of sensors
        """
        sensors = list(self._storage.values())

        # Apply status filter if provided
        if status_filter:
            sensors = [s for s in sensors if s['status'] == status_filter]

        sensors = list(self._storage.values())

        # Apply status filter if provided
        if status_filter:
            sensors = [s for s in sensors if s['status'] == status_filter]

        total = len(sensors)
        
        # Calculate pagination
        start = (page - 1) * per_page
        end = start + per_page
        
        return {
            'devices': devices[start:end],
            'total': total,
            'page': page,
            'per_page': per_page,
            'pages': (total + per_page - 1) // per_page,
            'status_filter': status_filter
        }
