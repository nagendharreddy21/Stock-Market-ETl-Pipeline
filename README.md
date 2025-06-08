** 📈 Stock Market Analytics & Alerting System (2020–2024)**
This project delivers a real-time stock market analytics pipeline that simulates daily stock data ingestion, calculates technical indicators, forecasts future prices, and triggers anomaly alerts using Prefect and email notifications. All outputs are visualized through a dynamic Power BI dashboard and a Streamlit-based machine learning prediction app.
**🔍 Why This Project?**
With growing uncertainty in stock markets, both analysts and investors need systems that provide:
- Timely insights into stock performance  
- Automatic alerting for unusual price or volume activity  
- Predictive tools to assist in investment decisions  
This end-to-end pipeline replicates a modern stock monitoring system — ideal for analysts, traders, or researchers who want real-time data intelligence without manual data handling.
**📊 Dashboard Goals**
The Power BI dashboard was developed to serve as the primary visual reporting layer for the project. It includes:

Latest Closing Price – Displays the most recent close for a selected stock  
Daily % Price Change – Tracks short-term shifts in market momentum  
RSI (14-Day Momentum) – Detects overbought (>70) or oversold (<30) conditions  
30-Day Price Volatility – Measures recent price fluctuation for risk assessment  
SMA-30 and SMA-200– Simple moving averages to assess trend direction  
Trading Volume vs. 20-Day Average – Highlights volume surges or drops  

All visualizations are filterable by ticker (AAPL, AMZN, GOOGL, META, MSFT) and time period (2020–2024) for deep exploratory analysis.


**⚠️ Anomaly Monitoring**
To ensure proactive awareness of risky or unusual stock behavior, the system sends alerts when:
- RSI moves beyond expected thresholds (e.g., > 80 or < 20)  
- Volatility exceeds historical average ranges  
- Daily % price change is highly abnormal (positive or negative)  
- ETL flow is interrupted or fails to simulate a new trading day  
These alerts are delivered via automated email notifications using a secure Gmail integration.

**🛠️ Data Source & Ingestion**
Source: Yahoo Finance historical data (via API)  
Time Range: January 2020 – December 2024  
Tickers: AAPL, AMZN, GOOGL, META, MSFT  
Storage: Data cleaned and structured into SQLite for analysis  
Simulation: The 2025 runtime simulates “live” daily rows from 2024 to test the pipeline’s real-time behavior and alerts  

**🧰 Tools & Technologies Used**
 Data Cleaning & Storage
- `pandas` and `numpy` for data wrangling and feature engineering  
- `sqlite3` to store structured data locally in a lightweight RDBMS  
 ETL & Automation
- `Prefect v3.4.4` used to orchestrate:
  - Simulated daily data ingestion
  - ETL pipeline execution into SQLite
  - Alert logic with condition-based triggers  
  - (No Airflow or external scheduler used)
 Alerting System
- `smtplib` for sending automated email alerts  
- `python-dotenv` to store Gmail credentials securely in a `.env` file  
- Threshold-based checks for RSI, volatility, and % price movement  

**Machine Learning**
- `Ridge Regression` trained on historical stock prices  
- Forecasts next-day closing price based on recent performance  
- Model developed in Jupyter Notebook  
- Saved as `ridge_model.pkl` and deployed in a **Streamlit** interface
- 
** Visualization**
  
- **Power BI** used as the primary dashboard tool  
- Live connection to SQLite enables real-time data refresh and interactivity
- ![Screenshot 2025-06-08 134916](https://github.com/user-attachments/assets/9de7e04c-3326-442b-9f52-9216152fd001)

 
**Stock Market Performance Dashboard**
This dashboard offers a quick, insightful overview of stock market trends and key performance indicators.
Key Features:
•	Interactive Charts: Visualize stock price trends and comparisons for select symbols (AAPL, AMZN, GOOG, META, MSFT).
•	Dynamic Symbol Selection: Filter data on charts by choosing specific stocks.
•	Essential KPIs: Instantly see the Top Loser, Highest Closing Price, Market Average Change, Active Symbols, Leading Sector, and Last Update Date.
•	Detailed Data Table: Access raw daily data for comprehensive review.
Purpose: Rapidly track individual stock performance and general market health.

> ✅ This project demonstrates skills across data engineering, statistical modeling, automation, visualization, and full-stack analytics — all applied to real-world financial data.
