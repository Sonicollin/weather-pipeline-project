SELECT
    city,
    AVG(temperature_2m) AS avg_temperature,
    MAX(temperature_2m) AS max_temperature,
    MIN(temperature_2m) AS min_temperature,
    AVG(wind_speed_10m) AS avg_wind_speed,
    COUNT(*) AS reading_count
FROM weather_data.current_weather
GROUP BY city