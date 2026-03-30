from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator


def start_task():
    print("DAG execution started")


def process_task():
    print("Data is being processed")


def finish_task():
    print("DAG execution finished")


with DAG(
    dag_id="basic_dataops_dag",
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,
    catchup=False,
) as dag:
    start = PythonOperator(
        task_id="start",
        python_callable=start_task,
    )

    process = PythonOperator(
        task_id="process",
        python_callable=process_task,
    )

    finish = PythonOperator(
        task_id="finish",
        python_callable=finish_task,
    )

    start >> process >> finish
