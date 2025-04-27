from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator

# Define the function that the task will execute
def say_hello():
    print("Hello from Airflow!")

# Default arguments for the DAG
default_args = {
    'owner': 'sumit',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
with DAG(
    'first_airflow_dag',          # DAG ID
    default_args=default_args,
    description='My First Airflow DAG',
    schedule_interval=None,       # No automatic schedule (manual trigger)
    start_date=datetime(2024, 4, 27),
    catchup=False,
    tags=['example'],
) as dag:

    task1 = PythonOperator(
        task_id='say_hello_task',
        python_callable=say_hello,
    )

    task1