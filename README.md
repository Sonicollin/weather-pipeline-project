# Weather Pipeline Project

A small, end-to-end ELT pipeline built as a learning project: extract weather data from a public API, validate it, transform it with SQL, containerize it, orchestrate it, and continuously verify it with CI.

See `TODO.md` for open items and possible extensions.

## What it does

1. **Extract & Load** — [`dlt`](https://dlthub.com/) pulls current weather readings for a set of cities from the [Open-Meteo](https://open-meteo.com/) API and loads them into a local DuckDB database.
2. **Validate** — each record is checked against a [Pydantic](https://docs.pydantic.dev/) model (`models.py`) before being loaded. Records that fail validation (bad types, out-of-range values) are skipped and logged rather than crashing the run.
3. **Transform** — [dbt](https://www.getdbt.com/) aggregates the raw readings into a `daily_weather_summary` view (per-city averages, min/max), and dbt tests (`unique`, `not_null`) guard against data-quality regressions.
4. **Containerize** — the whole extract → validate → transform flow runs inside a single Docker image, with output persisted via a mounted volume.
5. **Orchestrate** — an Apache Airflow instance (run separately via Docker Compose in `airflow_setup/`) schedules and triggers the pipeline's Docker image using `DockerOperator`.
6. **CI** — a GitHub Actions workflow rebuilds the image and reruns the pipeline (including dbt tests) on every push to `main`, catching breakages before they'd ever reach a scheduled run.

## Project structure

```
.
├── src/
│   └── weather_pipeline/
│       ├── __init__.py
│       ├── models.py         # Pydantic data contract for a weather reading
│       └── pipeline.py       # dlt resource + extraction/load logic
├── pyproject.toml            # Package metadata, installed in editable mode for local dev
├── Dockerfile
├── docker-compose.yml        # Local run + volume mount for persistent output
├── requirements.txt
├── weather_transforms/       # dbt project (models, tests, profiles)
├── airflow_setup/            # Standalone Airflow-via-Docker-Compose setup + DAGs
└── .github/workflows/ci.yml  # Build + test on every push
```

## Running it locally

**Just the pipeline:**

```bash
docker compose up --build
```

Output (a fresh `weather_pipeline.duckdb`) lands in `./output/`.

**With orchestration:**

1. Build the pipeline image first: `docker compose build`
2. Start Airflow from `airflow_setup/`: `docker compose up -d`
3. Open `http://localhost:8080` (login: `airflow` / `airflow`) and trigger `weather_pipeline_dag`.

## What this project is not

This is a learning project, not a production system. The Airflow setup is Apache's own "quick-start" configuration (explicitly not intended for production use), and there's no secrets management, retry tuning, or monitoring beyond what's described above.
