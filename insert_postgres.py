# stock_etl_pipeline.py

import os
import json
import time
import requests
import psycopg2
from pymongo import MongoClient
from dotenv import load_dotenv

# ------------------------------
# STEP 1: Setup
# ------------------------------
load_dotenv()
API_KEY = os.getenv("API_KEY")
SYMBOLS = ["AAPL", "MSFT", "GOOG", "AMZN", "META"]

# ------------------------------
# STEP 2: Fetch Historical Stock Data
# ------------------------------
def fetch_full_history(symbol):
    url = f"https://financialmodelingprep.com/api/v3/historical-price-full/{symbol}?apikey={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        print(f"✅ Historical data fetched for {symbol}")
        return response.json().get("historical", [])
    else:
        print(f"❌ Failed to fetch {symbol}: {response.status_code}")
        return []

stock_history = {}
for i, symbol in enumerate(SYMBOLS):
    print(f"[{i+1}/{len(SYMBOLS)}] Fetching data for {symbol}")
    stock_history[symbol] = fetch_full_history(symbol)
    time.sleep(1)

# Save JSON
with open("full_stock_history.json", "w", encoding="utf-8") as f:
    json.dump(stock_history, f, indent=2)
print("📁 Saved historical data to full_stock_history.json")

# ------------------------------
# STEP 3: Fetch Company Profile Info
# ------------------------------
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
    print(f"⚠️ Failed to fetch profile for {symbol}")
    return {"symbol": symbol, "sector": "N/A", "industry": "N/A"}

company_profiles = [fetch_company_profile(s) for s in SYMBOLS]
print("✅ Company profile data fetched")

# ------------------------------
# STEP 4: Insert Stock Data into PostgreSQL
# ------------------------------
try:
    conn = psycopg2.connect(
        dbname="StockMarket",
        user="postgres",
        password="1821",
        host="localhost",
        port="5432"
    )
    cur = conn.cursor()

    cur.execute("""
    DROP TABLE IF EXISTS stock_quotes;
    CREATE TABLE stock_quotes (
        id SERIAL PRIMARY KEY,
        symbol TEXT,
        date TEXT,
        open NUMERIC,
        high NUMERIC,
        low NUMERIC,
        close NUMERIC,
        adj_close NUMERIC,
        volume BIGINT,
        unadjusted_volume BIGINT,
        change NUMERIC,
        change_percent NUMERIC,
        vwap NUMERIC,
        label TEXT,
        change_over_time NUMERIC
    );
    """)
    conn.commit()

    for symbol in SYMBOLS:
        records = stock_history.get(symbol, [])
        print(f"Inserting {len(records)} records for {symbol}")
        for record in records:
            cur.execute("""
                INSERT INTO stock_quotes (
                    symbol, date, open, high, low, close, adj_close, volume,
                    unadjusted_volume, change, change_percent, vwap, label, change_over_time
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                symbol,
                record.get("date"),
                record.get("open"),
                record.get("high"),
                record.get("low"),
                record.get("close"),
                record.get("adjClose"),
                record.get("volume"),
                record.get("unadjustedVolume"),
                record.get("change"),
                record.get("changePercent"),
                record.get("vwap"),
                record.get("label"),
                record.get("changeOverTime")
            ))
    conn.commit()
    conn.close()
    print("✅ Stock data inserted into PostgreSQL")

except Exception as e:
    print(f"❌ PostgreSQL error: {e}")

# ------------------------------
# STEP 5: Insert Profile Data into MongoDB
# ------------------------------
try:
    client = MongoClient("mongodb://localhost:27017/")
    db = client["stocks"]
    collection = db["profiles"]
    collection.delete_many({})  # clear old data
    collection.insert_many(company_profiles)
    print("✅ Company profiles inserted into MongoDB")
except Exception as e:
    print(f"❌ MongoDB error: {e}")
