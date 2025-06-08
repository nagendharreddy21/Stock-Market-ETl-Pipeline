from pymongo import MongoClient
import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")
SYMBOLS = ["AAPL", "MSFT", "GOOG", "AMZN", "META"]

def fetch_profile(symbol):
    url = f"https://financialmodelingprep.com/api/v3/profile/{symbol}?apikey={API_KEY}"
    r = requests.get(url)
    if r.status_code == 200:
        data = r.json()
        if data:
            return {
                "symbol": symbol,
                "sector": data[0].get("sector", "N/A"),
                "industry": data[0].get("industry", "N/A")
            }
    return {"symbol": symbol, "sector": "N/A", "industry": "N/A"}

profiles = [fetch_profile(s) for s in SYMBOLS]

client = MongoClient("mongodb://localhost:27017/")
db = client["stocks"]
collection = db["profiles"]

collection.delete_many({})  # clear old
collection.insert_many(profiles)

print("✅ Inserted profiles into MongoDB")
