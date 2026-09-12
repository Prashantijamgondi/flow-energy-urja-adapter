"""
Pydantic response models for the CLEAN api we expose.
These describe OUR contract, not the portal's raw shape.
Adjust field names/types once you see the real data (dates, numeric fields, etc).
"""
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class MeterSummary(BaseModel):
    meter_id: str
    serial_number: Optional[str] = None
    status: Optional[str] = None
    location: Optional[str] = None


class MeterDetail(MeterSummary):
    installed_at: Optional[datetime] = None
    last_reading_at: Optional[datetime] = None
    raw_fields: Optional[dict] = None  # escape hatch for anything not yet modeled


class ConsumptionPoint(BaseModel):
    timestamp: datetime
    value_kwh: float


class ConsumptionHistory(BaseModel):
    meter_id: str
    points: List[ConsumptionPoint]


class HierarchyNode(BaseModel):
    id: str
    name: str
    type: str  # e.g. "feeder", "dtr", "meter"
    children: List["HierarchyNode"] = []


HierarchyNode.model_rebuild()


class LoginRequest(BaseModel):
    username: str
    password: str


class HealthResponse(BaseModel):
    status: str
    portal_reachable: bool
