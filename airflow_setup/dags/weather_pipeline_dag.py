from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from datetime import datetime

with DAG(
    dag_id = "weather_pipeline_dag",
    schedule = "@daily",
    start_date = datetime(2025, 1, 1),
    catchup = False,
) as dag:

    run_weather_pipeline = DockerOperator(
        task_id = "run_weather_pipeline",
        image = "weather_pipeline",
        api_version = "auto",
        auto_remove = "success",
        docker_url = "unix://var/run/docker.sock",
        network_mode = "bridge",
        mount_tmp_dir = False,
    )