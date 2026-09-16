# TODO / Project Log

A running record of what this project set out to teach, what's done, and what's still open.

## Phase 3 — Ingestion & Data Quality

- [x] Extract weather data from the Open-Meteo REST API using `dlt`
- [x] Validate incoming records with Pydantic (`WeatherReading` model: types + `Field` constraints)
- [x] Skip and log invalid records instead of crashing the whole pipeline run
- [x] Load raw records into a local DuckDB destination via `dlt`
- [x] Transform raw data into `daily_weather_summary` using a dbt SQL model
- [x] Add dbt tests (`unique`, `not_null`) and use them to catch a real historical data-quality bug
- [x] Understand and fix a real dlt local-state bug (pipeline name tied to cached destination path)

## Phase 4 — Containerization, Orchestration, CI/CD

- [x] Containerize the pipeline (`Dockerfile`, `.dockerignore`, pinned `requirements.txt`)
- [x] Persist pipeline output across container runs via a mounted volume
- [x] Simplify local runs with `docker-compose.yml`
- [x] Stand up Apache Airflow locally via Docker Compose
- [x] Build a DAG using `DockerOperator` to run the pipeline image on a schedule
- [x] Set up GitHub Actions CI: build the image and run the pipeline + dbt tests on every push to `main`

## Known loose ends / cleanup

- [ ] Delete the malformed `output;C` folder (leftover from an earlier Windows path-mounting issue)
- [ ] Confirm `weather_pipeline.duckdb` and `__pycache__/` are not still tracked by Git from before `.gitignore` existed (`git status` check; `git rm --cached` if needed)
- [ ] Remove stale/duplicate local Docker images no longer in use
- [ ] Bump `actions/checkout@v4` to the current major version in the CI workflow
- [ ] Decide on and execute a proper Python package layout (deferred from Phase 4; scratch files like early tutorial scripts should be separated from the real pipeline)

## Possible next steps (not started)

- [ ] Push the built image to a container registry (e.g. GitHub Container Registry) so Airflow could pull an updated image automatically instead of relying on a local build
- [ ] Add `dlt` incremental loading to avoid duplicate rows on repeated runs within a short window
- [ ] Expand dbt tests beyond `unique`/`not_null` (e.g. accepted value ranges, referential checks)
- [ ] Revisit Dagster as a point of comparison against Airflow, now that the orchestration concepts are solid
