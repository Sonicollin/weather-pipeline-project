import dlt
import requests
import duckdb
import os
from models import WeatherReading

print("Running from:", os.getcwd())

LOCATIONS = {
    "Okinawa": (26.5, 127.9),
    "Tokyo": (35.7, 139.7),
    "Sapporo": (43.1, 141.3)
}

@dlt.resource
def current_weather():
    for city, (lat, lon) in LOCATIONS.items():
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": lat,
            "longitude": lon,
            "current": "temperature_2m,wind_speed_10m,relative_humidity_2m"
        }
        response = requests.get(url, params=params)
        data = response.json()["current"]
        data["city"] = city

        try:
            reading = WeatherReading(**data)
            yield reading.model_dump()
        except Exception as e:
            print(f"Skipping invalid record for {city}: {e}")

pipeline = dlt.pipeline(
    pipeline_name = "weather_pipeline",
    destination = dlt.destinations.duckdb("output/weather_pipeline.duckdb"),
    dataset_name = "weather_data"
)

load_info = pipeline.run(current_weather())
print(load_info)


with duckdb.connect("output/weather_pipeline.duckdb") as conn:
    result = conn.sql("SELECT * FROM weather_data.current_weather")
    print(result)