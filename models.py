from pydantic import BaseModel, Field

class WeatherReading(BaseModel):
    time: str
    interval: int
    temperature_2m: float = Field(ge=-50, le=60)
    wind_speed_10m: float = Field(ge=0)
    relative_humidity_2m: int = Field(ge=0, le=100)
    city: str = Field(min_length=1)