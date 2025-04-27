import requests
from airflow import DAG
from airflow.models import Variable
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta, timezone
import psycopg2

def extract():
    api_key = Variable.get("COINDESK_API_KEY")
    url = "https://data-api.coindesk.com/index/cc/v1/latest/tick"
    params = {
        "market": "ccix",
        "instruments": "BTC-USD",
        "api_key": api_key
    }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        print("Data fetched successfully!")
        return data   # This is automatically pushed to XCom
    else:
        raise Exception(f"Failed to fetch data. Status Code: {response.status_code}")

def transform(**kwargs):
    ti = kwargs['ti']  # ti = task instance

    # Pull extracted data from previous task
    extracted_data = ti.xcom_pull(task_ids='extract_task')

    if not extracted_data:
        raise ValueError("No data fetched from extract task!")

    
    transformed_data = {
        "price": extracted_data['Data']['BTC-USD']['VALUE'],  # Example: depends on your actual API response structure
        "timestamp": datetime.fromtimestamp(
            extracted_data['Data']['BTC-USD']['VALUE_LAST_UPDATE_TS'],
            tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
    }

    print("Data transformed successfully!")
    return transformed_data  # Will be pushed to XCom again for next task

def load(**kwargs):
    ti = kwargs['ti']
    transformed_data = ti.xcom_pull(task_ids='transform_task')

    if not transformed_data:
        raise ValueError("No transformed data found!")

    # Connect to Postgres DB
    conn = psycopg2.connect(
        host="postgres",       # Same as service name in docker-compose.yml
        database=Variable.get("POSTGRES_DB"),
        user=Variable.get("POSTGRES_USER"),
        password=Variable.get("POSTGRES_PASSWORD")
    )
    cursor = conn.cursor()

    # Insert the data
    insert_query = """
    INSERT INTO btc_price (price, timestamp) VALUES (%s, %s)
    """
    cursor.execute(insert_query, (transformed_data['price'], transformed_data['timestamp']))

    conn.commit()
    cursor.close()
    conn.close()

    print("Data loaded into Postgres successfully!")

# Default arguments for DAG
default_args = {
    'owner': 'sumit',
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)

}

# Define the DAG
with DAG(
    'etl_pipeline_dag',
    default_args=default_args,
    description='ETL pipeline that extracts, transforms and loads data',
    schedule_interval=None,  # We'll trigger manually first
    start_date=datetime(2025, 4, 27),
    catchup=False,
) as dag:

    # Define Tasks
    extract_task = PythonOperator(
        task_id='extract_task',
        python_callable=extract,
    )

    transform_task = PythonOperator(
        task_id='transform_task',
        python_callable=transform,
        provide_context=True,
    )

    load_task = PythonOperator(
        task_id='load_task',
        python_callable=load,
        provide_context=True,
    )

    # Set task dependencies
    extract_task >> transform_task >> load_task