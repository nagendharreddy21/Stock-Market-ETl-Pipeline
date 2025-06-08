import requests
import json
import os
import time
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
API_KEY = os.getenv("API_KEY")

SYMBOLS = ["AAPL", "MSFT", "GOOG", "AMZN", "META"]

def fetch_full_history(symbol):
    url = f"https://financialmodelingprep.com/api/v3/historical-price-full/{symbol}?apikey={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        print(f"✅ Fetched data for {symbol}")
        data = response.json()
        return data.get("historical", [])
    else:
        print(f"❌ Failed to fetch {symbol}: {response.status_code}")
        return []

stock_data = {}

for i, symbol in enumerate(SYMBOLS):
    print(f"[{i+1}/{len(SYMBOLS)}] Fetching history for {symbol}...")
    history = fetch_full_history(symbol)
    stock_data[symbol] = history
    time.sleep(1)  # avoid rate limiting

# Save the data
with open("full_stock_history.json", "w", encoding="utf-8") as f:
    json.dump(stock_data, f, indent=2)

print("📁 Saved to full_stock_history.json")
