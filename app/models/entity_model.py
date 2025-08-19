from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from bson import ObjectId

# Embedded Documents
# --------------------------------

class Sensor(BaseModel):
    type: str
    model: str
    calibrationDate: datetime
    status: bool


class Metadata(BaseModel):
    installationDate: datetime


class Tool(BaseModel):
    type: str
    model: str
    status: bool


class ReadingValue(BaseModel):
    value: float
    status: int
    unit: str


class SensorReadings(BaseModel):
    turbidity: Optional[ReadingValue]
    tds: Optional[ReadingValue]
    ph: Optional[ReadingValue]
    temperature: Optional[ReadingValue]
    distance: Optional[ReadingValue]
    uv: Optional[ReadingValue]
    flow: Optional[ReadingValue]


class CalibrationReading(BaseModel):
    expected: float
    actual: float
    unit: str




# Class Main
# ------------------------

class Device(BaseModel):
    id: ObjectId = Field(default_factory=ObjectId, alias="_id")
    deviceId: str
    name: str
    sensors: List[Sensor] = []
    metadata: Optional[Metadata]
    tools: List[Tool] = []


class SensorData(BaseModel):
    id: ObjectId = Field(default_factory=ObjectId, alias="_id")
    deviceId: str
    timestamp: datetime
    readings: SensorReadings


class Calibration(BaseModel):
    id: ObjectId = Field(default_factory=ObjectId, alias="_id")
    deviceId: str
    sensorType: str
    timestamp: datetime
    readings: List[CalibrationReading]
