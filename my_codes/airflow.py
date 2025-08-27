from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator

from my_codes.math_task import run_addition

def airflow_run_addition(**context):
    return run_addition(5, 7)   # hardcoded or from Variables/XCom

with DAG(
    dag_id="simple_math_dag",
    start_date=datetime(2025, 8, 27),
    schedule_interval=None,
    catchup=False,
) as dag:

    task_add = PythonOperator(
        task_id="add_numbers_task",
        python_callable=airflow_run_addition,
        provide_context=True,
    )
