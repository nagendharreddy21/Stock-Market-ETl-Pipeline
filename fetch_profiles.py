import requests
import os
import pandas as pd
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")

SYMBOLS = ["AAPL", "MSFT", "GOOG", "AMZN", "META"]

def fetch_company_profile(symbol):
    url = f"https://financialmodelingprep.com/api/v3/profile/{symbol}?apikey={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data and isinstance(data, list):
            return {
                "symbol": symbol,
                "sector": data[0].get("sector", "N/A"),
                "industry": data[0].get("industry", "N/A")
            }
    return {"symbol": symbol, "sector": "N/A", "industry": "N/A"}

# Fetch all
company_profiles = [fetch_company_profile(symbol) for symbol in SYMBOLS]
df = pd.DataFrame(company_profiles)
print(df)
