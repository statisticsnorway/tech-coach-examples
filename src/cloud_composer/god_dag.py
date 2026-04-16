from datetime import datetime

from airflow.sdk import dag, task


@dag(
    dag_id="god_dag",
    start_date=datetime(2026, 4, 10),
    schedule="@hourly",
    catchup=False,
    tags=["demo"],
)
def god_dag():
    @task
    def greet() -> None:
        current_time = datetime.now().strftime("%H:%M:%S")
        print(f"God dag, klokken er {current_time}")

    greet()


god_dag()
