# ETL Pipeline with Airflow, Docker and PostgreSQL

📦 Project Overview

This project sets up a complete ETL (Extract-Transform-Load) pipeline using:
* Apache Airflow for orchestration
* Docker Compose for containerized deployment
* PostgreSQL for data storage
* Coindesk API to fetch Bitcoin price data

---

🛠️ Stack Used

* Python 3.8
* Apache Airflow 2.7+
* PostgreSQL 13+
* Docker & Docker Compose

---

## 📦 Project Structure
```
etl-pipeline-docker-postgres/
│
├── airflow/
│   ├── dags/
│   │   ├── etl_dag.py                 # Main ETL DAG
│   │   └── first_dag.py               # Sample Hello World DAG
│   └── docker-compose.yml             # Airflow Docker Compose configuration
│
├── etl/
│   ├── main.py                        # ETL script
│   ├── requirements.txt               # Python dependencies
│   └── .env                           # Environment variables (not in version control)
│
├── Dockerfile                         # Docker image configuration
├── docker-compose.yml                 # Main Docker Compose configuration
├── .gitignore                         # Git ignore rules
└── README.md                          # Project documentation
```
---

## ⚙️ Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone https://github.com/sumitsingwal/etl-pipeline-docker-postgres.git
   cd etl-pipeline-docker-postgres

2. Start the Services
    cd airflow
    docker-compose up -d

3.	Access Airflow UI
    Visit: http://localhost:8080

4. Create Admin User (first-time only)
    docker-compose exec webserver airflow users create \
        --username admin \
        --firstname {First_Name} \
        --lastname {Last_Name} \
        --role Admin \
        --email you@example.com \
        --password admin

5. Set Airflow Variables In Airflow
    UI > Admin > Variables:
    * COINDESK_API_KEY → your real API key
    * POSTGRES_DB → airflow
    * POSTGRES_USER → etl_user
    * POSTGRES_PASSWORD → etl_pass

📊 ETL DAG: etl_pipeline_dag

This DAG performs the following steps:

1. Extract Bitcoin price data from the Coindesk API.

2. Transform it to include only relevant fields and format timestamps.

3. Load the cleaned data into a Postgres table btc_price.

Sample Table Schema
CREATE TABLE btc_price (
    id SERIAL PRIMARY KEY,
    price FLOAT,
    timestamp TIMESTAMP
);
