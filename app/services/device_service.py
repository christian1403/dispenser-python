"""
Device Service for handling business logic
"""

import uuid
from datetime import datetime
from app.models.device_model import DeviceModel
from app.utils.helpers import generate_uuid, current_timestamp
from app.utils.database import DatabaseMongo
from bson import ObjectId

dbDevices = DatabaseMongo.db.devices
class DeviceService:
    """Service class for handling device-related operations"""
    
    def __init__(self):
        """Initialize the service with in-memory storage (replace with database)"""
    def get_all_devices(self):
        """
        Get all device data
        
        Returns:
            List of device data
        """

        docs = dbDevices.find()
        if docs:
            devices = [DeviceModel.from_mongo(doc).dict() for doc in docs]
            return {"devices": devices}
        return []
    
    def create_device(self, data):
        """
        Create a new device
        
        Args:
            data: Dictionary containing device data
            
        Returns:
            Created device data
        """
        check = dbDevices.find_one({"device_id": data.get("device_id")})
        if check:
            raise ValueError("Device with this ID already exists")

        device = {
            "device_id" : data.get("device_id"),
            "name" : data.get("name"),
            "sensors" : data.get("sensors"),
            "metadata" : data.get("metadata"),
            "tools" : data.get("tools")
        }
        
        result = dbDevices.insert_one(device)
        inserted_doc = dbDevices.find_one({"_id" : result.inserted_id})
        return {"device": DeviceModel.from_mongo(inserted_doc).dict()}

    def get_device_by_id(self, device_id):
        """
        Get device by ID
        
        Args:
            device_id: ID of the device
            
        Returns:
            Device data or None if not found
        """

        device = dbDevices.find_one({"device_id": device_id})
        if device:
            return {"device": DeviceModel.from_mongo(device).dict()}
        return None

    def update_device(self, device_id, data):
        """
        Update device by ID
        
        Args:
            device_id: ID of the device
            data: Updated data
            
        Returns:
            Updated device data or None if not found
        """
        device = dbDevices.find_one({"device_id": device_id})
        if not device:
            return None

        device_data = DeviceModel.from_mongo(device).dict()


        # Update fields
        update_data = {
            "name" : data.get("name", device_data['name']),
            "sensors" : data.get("sensors", device_data['sensors']),
            "tools" : data.get("tools", device_data['tools'])
        }

        dbDevices.update_one({"device_id": device_id}, {"$set": update_data})

        deviceUpdated = dbDevices.find_one({"device_id": device_id})
        return {"device": DeviceModel.from_mongo(deviceUpdated).dict()}

    def delete_device(self, device_id):
        """
        Delete device by ID
        
        Args:
            device_id: ID of the device
            
        Returns:
            Boolean indicating success
        """
        device = dbDevices.find_one({"device_id": device_id})
        if not device:
            return False
        dbDevices.delete_one({"device_id": device_id})

        return {"device": DeviceModel.from_mongo(device).dict()}

    def list_devices(self, page=1, per_page=10, status_filter=None):
        """
        List devices with pagination and optional status filter
        
        Args:
            page: Page number
            per_page: Items per page
            status_filter: Optional status filter
            
        Returns:
            Paginated list of devices
        """
        devices = list(self._storage.values())
        
        # Apply status filter if provided
        if status_filter:
            devices = [d for d in devices if d['status'] == status_filter]
        
        total = len(devices)
        
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
