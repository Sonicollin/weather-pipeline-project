FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONPATH=/app/src

CMD ["sh", "-c", "python -m weather_pipeline.pipeline && cd dbt_project && dbt run --profiles-dir ."]