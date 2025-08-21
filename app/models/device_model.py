from pydantic import BaseModel

class DeviceModel(BaseModel):
    id: str
    device_id: str
    name: str
    sensors: dict
    metadata: dict
    tools: list

    @staticmethod
    def from_mongo(doc):
        return DeviceModel(
            id=str(doc["_id"]),
            device_id=doc.get("device_id"),
            name=doc.get("name"),
            sensors=doc.get("sensors", []),
            metadata=doc.get("metadata", {}),
            tools=doc.get("tools", [])
        )
