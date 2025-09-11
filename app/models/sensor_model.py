from pydantic import BaseModel

class SensorModel(BaseModel):
    id: str
    device_id: str
    timestamp: str
    sensor_type: str 
    unit: str
    value: float
    status: int

    @staticmethod
    def from_mongo(doc):
        return SensorModel(
            id=str(doc["_id"]),
            device_id=doc.get("device_id"),
            timestamp=doc.get("timestamp"),
            sensor_type=doc.get("sensor_type"),
            unit=doc.get("unit"),
            value=doc.get("value"),
            status=doc.get("status", 0)
        )
