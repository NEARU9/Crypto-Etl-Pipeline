# Crypto-ETL-Pipeline

End-to-end ETL pipeline that extracts cryptocurrency data from the CoinGecko API, transforms it using pandas, stores it in PostgreSQL, and visualizes it with an interactive Streamlit dashboard.

---

## 🌐 Live Dashboard

You can view the live dashboard here:

🔗 <a href="https://crypto-etl-pipeline-reza.streamlit.app/" target="_blank" rel="noopener noreferrer">Crypto ETL Pipeline Dashboard</a>

---
## 🚀 Project Overview

This project demonstrates a **complete cryptocurrency data pipeline**:

1. **Extract** Bitcoin market data from CoinGecko API
2. **Transform** the data using Python & pandas
3. **Load** the processed data into a PostgreSQL database
4. **Visualize** the data using a Streamlit interactive dashboard with Plotly charts

This project is designed to showcase **ETL pipeline development, data engineering skills, and interactive data visualization**.

---

## 📊 Dashboard Preview

![Bitcoin Dashboard](Dashboard.png)

---

## 🏗 Architecture

```
CoinGecko API
      ↓
Python ETL (Pandas)
      ↓
PostgreSQL Database
      ↓
Streamlit Dashboard
```

---

## ⚙️ Technologies Used

* Python
* Pandas
* PostgreSQL
* SQLAlchemy
* Streamlit
* Plotly
* Jupyter Notebook

---

## 📂 Project Structure

```
Crypto-ETL-Pipeline/
│
├── fetch_crypto.ipynb      # Jupyter Notebook for ETL process
├── Dashboard.py            # Streamlit dashboard script
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
│
├── images/
│   └── dashboard.png       # Dashboard screenshot
```

---

## 🔧 Installation

### 1. Clone Repository

```
git clone https://github.com/yourusername/Crypto-ETL-Pipeline.git
cd Crypto-ETL-Pipeline
```

### 2. Install Dependencies

```
pip install -r requirements.txt
```

### 3. Setup PostgreSQL

Make sure PostgreSQL is installed and running.

Create a database:

```
CREATE DATABASE crypto_pipeline;
```

Update the database connection credentials in **fetch_crypto.ipynb** or **Dashboard.py** if necessary.

---

# 📝 ETL Process

## 1️⃣ Extract Data

Fetch Bitcoin market data from the CoinGecko API.

Example:

```
import requests

data = requests.get(
    "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart",
    params={"vs_currency": "usd", "days": "360"}
).json()
```

---

## 2️⃣ Transform Data

Data processing steps using **pandas**:

* Convert API JSON response into pandas DataFrame
* Merge price, market cap, and volume data
* Convert timestamp to datetime format
* Select important columns:

  * date
  * price
  * market_cap
  * volume
* Sort data by date

---

## 3️⃣ Load Data

Store processed data into PostgreSQL using SQLAlchemy.

Example:

```
from sqlalchemy import create_engine

engine = create_engine(
    "postgresql://username:password@localhost:5432/crypto_pipeline"
)

df.to_sql("bitcoin_market", engine, if_exists="replace", index=False)
```

---

## 4️⃣ Data Visualization

Data is visualized using **Streamlit** and **Plotly** with interactive charts.

Dashboard features include:

* Bitcoin price trend
* Moving average analysis
* Market capitalization
* Trading volume
* Price distribution

Additional metrics:

* Current price
* Highest price
* Lowest price
* Average price

Users can also **download filtered data as CSV**.

---

# ▶️ Run the Dashboard

Run the Streamlit dashboard with:

```
streamlit run Dashboard.py
```

Then open the local URL shown in the terminal to view the dashboard.

---

# 🎯 Key Features

* Real-time Bitcoin price visualization
* Moving average analysis
* Market capitalization tracking
* Trading volume charts
* Downloadable dataset (CSV)
* Interactive filters:

  * Date range
  * Chart theme
  * Moving average window

---

# 👤 Author

**Rahmat Reza Kurniawan**

Data Engineer

---

# 📚 References

* CoinGecko API Documentation
* Streamlit Documentation
* Plotly Documentation
* SQLAlchemy Documentation
