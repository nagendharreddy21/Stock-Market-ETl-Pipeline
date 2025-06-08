from fastapi import FastAPI
import psycopg2
import logging
from pymongo import MongoClient

# Setup basic logging configuration
logging.basicConfig(level=logging.INFO)

app = FastAPI()

def get_latest_stock(symbol):
    try:
        conn = psycopg2.connect(
            dbname="StockMarket",
            user="postgres",
            password="1821",
            host="localhost"
        )
        cur = conn.cursor()
        cur.execute("""
            SELECT symbol, date, open, close
            FROM latest_quotes
            WHERE symbol = %s
        """, (symbol,))
        row = cur.fetchone()
        conn.close()

        if row:
            date_value = row[1]
            # Check if date_value is a datetime object before formatting
            if hasattr(date_value, "strftime"):
                date_str = date_value.strftime("%Y-%m-%d")
            else:
                date_str = str(date_value)

            return {
                "symbol": row[0],
                "date": date_str,
                "open": float(row[2]),
                "close": float(row[3])
            }
        return {"error": "Symbol not found"}

    except Exception as e:
        logging.error(f"Error in get_latest_stock: {e}")
        return {"error": str(e)}

@app.get("/")
def home():
    return {"message": "Welcome to the Stock Analytics API"}

@app.get("/stock/{symbol}")
def stock(symbol: str):
    return get_latest_stock(symbol.upper())

@app.get("/profile/{symbol}")
def get_company_profile(symbol: str):
    try:
        client = MongoClient("mongodb://localhost:27017/")
        db = client["stocks"]
        collection = db["profiles"]
        result = collection.find_one({"symbol": symbol.upper()}, {"_id": 0})
        
        if result:
            return result
        else:
            return {"error": "Company profile not found"}
    except Exception as e:
        logging.error(f"Error in get_company_profile: {e}")
        return {"error": str(e)}
