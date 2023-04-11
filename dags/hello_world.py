from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator

def print_hello():
    return "Hello World!"

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=1),
}

dag = DAG(
    "hello_world",
    description="Simple Hello World DAG",
    schedule_interval="0 * * * *",
    start_date=datetime(2023, 4, 11),
    catchup=False,
    default_args=default_args,
)

t1 = PythonOperator(
    task_id="print_hello",
    python_callable=print_hello,
    dag=dag,
)
