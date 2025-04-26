import requests
import os
import psycopg2
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

def extract():
    api_key = os.getenv("COINDESK_API_KEY")
    url = "https://data-api.coindesk.com/index/cc/v1/latest/tick"
    params = {
        "market": "ccix",
        "instruments": "BTC-USD",
        "api_key": api_key
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data["Data"]["BTC-USD"]["VALUE"]



def main():
    price = extract()
    print("Bitcoin Price (USD):", price)
    #load_to_postgres(price)

if __name__ == "__main__":
    main()