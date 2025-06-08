import streamlit as st
from neuralprophet import NeuralProphet
import pandas as pd
import requests
import datetime
import matplotlib.pyplot as plt

# -- App UI --
st.title("📈 Stock Price Predictor (AAPL)")
st.markdown("Using NeuralProphet to forecast future stock prices")

# -- Fetch historical data from API --
API_KEY = "ZYErZXiO23ScdSjECf8TMJPDlvZ4YcvN"  # Replace with your real API key
symbol = "AAPL"

@st.cache_data
def load_stock_data(symbol):
    url = f"https://financialmodelingprep.com/api/v3/historical-price-full/{symbol}?apikey={API_KEY}"
    r = requests.get(url)
    data = r.json()["historical"]
    df = pd.DataFrame(data)
    df = df[["date", "close"]]
    df.rename(columns={"date": "ds", "close": "y"}, inplace=True)
    df["ds"] = pd.to_datetime(df["ds"])
    df.sort_values("ds", inplace=True)
    return df

df = load_stock_data(symbol)
st.subheader("Historical Close Prices")
st.line_chart(df.set_index("ds")["y"])

# -- Forecasting --
periods = st.slider("Days to Predict", 7, 90, 30)
model = NeuralProphet()
model.fit(df, freq="D", epochs=100)

future = model.make_future_dataframe(df, periods=periods)
forecast = model.predict(future)

st.subheader("🔮 Forecast")
fig_forecast = model.plot(forecast)
st.pyplot(fig_forecast)

st.subheader("📊 Forecast Components")
fig_components = model.plot_components(forecast)
st.pyplot(fig_components)
