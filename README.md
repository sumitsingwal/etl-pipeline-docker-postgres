# ETL Pipeline with Docker and PostgreSQL

This project demonstrates a simple ETL (Extract, Transform, Load) pipeline using Python, Docker, and PostgreSQL.  
It extracts real-time Bitcoin price data from the Coindesk API, processes it, and loads it into a PostgreSQL database — all containerized using Docker Compose.

---

## 🚀 Technologies Used
- Python 3.10
- Docker
- Docker Compose
- PostgreSQL
- psycopg2 (Python PostgreSQL adapter)

---

## 📦 Project Structure
etl-pipeline-docker-postgres/
├── etl/
│   ├── main.py
│   ├── requirements.txt
│   └── .env (not pushed to GitHub)
├── Dockerfile
├── docker-compose.yml
├── .gitignore
├── README.md

---

## ⚙️ Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone https://github.com/sumitsingwal/etl-pipeline-docker-postgres.git
   cd etl-pipeline-docker-postgres

2. Create .env File
    Inside the etl/ folder, create a .env file with:
    COINDESK_API_KEY=your_coindesk_api_key
    DB_HOST=db
    DB_USER=etl_user
    DB_PASSWORD=etl_pass
    DB_NAME=etl_db

3. Build and Start the Containers
    docker-compose up --build

4.	Verify Data Insertion
    •	Access the PostgreSQL database inside the container:

    docker exec -it etl_postgres psql -U etl_user -d etl_db

    •	Run:

    SELECT * FROM bitcoin_prices;

🔄 How the ETL Process Works
	•	Extract: Connects to Coindesk API and retrieves the latest Bitcoin price.
	•	Transform: Parses and cleans the response.
	•	Load: Inserts the price and a timestamp into the PostgreSQL bitcoin_prices table.

🌱 Future Enhancements
	•	Integrate Apache Airflow to schedule and orchestrate the ETL pipeline.
	•	Add error handling and retries for API failures.
	•	Build a simple dashboard to visualize Bitcoin price trends over time.