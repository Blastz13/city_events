from pydantic import BaseModel, Field


class EventByCoordinatesRequest(BaseModel):
    longitude: float = Field(..., description="longitude")
    latitude: float = Field(..., description="latitude")
