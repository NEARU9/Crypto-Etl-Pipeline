import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
import requests

# Page configuration
st.set_page_config(
    page_title="Bitcoin Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS
st.markdown("""
    <style>
    /* Main container styling */
    .main {
        padding: 0rem 1rem;
    }
    
    /* Title styling */
    .title {
        text-align: center;
        padding: 1rem;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    
    /* Metric card styling */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        text-align: center;
        transition: transform 0.3s;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
    }
    
    /* Info box styling */
    .info-box {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
    }
    
    /* Table styling */
    .dataframe {
        font-size: 0.9rem;
        border-collapse: collapse;
        width: 100%;
    }
    
    .dataframe th {
        background-color: #667eea;
        color: white;
        padding: 0.75rem;
        text-align: left;
    }
    
    .dataframe td {
        padding: 0.75rem;
        border-bottom: 1px solid #dee2e6;
    }
    
    .dataframe tr:hover {
        background-color: #f5f5f5;
    }
    </style>
""", unsafe_allow_html=True)

# # Fungsi untuk koneksi database dengan caching
# @st.cache_data(ttl=3600)  # Cache 1 jam
# def load_data():
#     """Load data dari PostgreSQL dengan caching"""
#     try:
#         engine = create_engine("postgresql://postgres:RezaReza@localhost:5432/crypto_pipeline")
#         df = pd.read_sql("SELECT * FROM bitcoin_market ORDER BY date", engine)
#         return df
#     except Exception as e:
#         st.error(f"Error connecting to database: {e}")
#         return pd.DataFrame()

def extract_bitcoin_data():
    """Extract langsung dari API"""
    url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"
    params = {
        "vs_currency": "usd",
        "days": "360"
    }
    response = requests.get(url, params=params)
    return response.json()

def transform_bitcoin_data(data):
    """Transform data dari API"""
    prices = data["prices"]
    market_caps = data["market_caps"]
    volumes = data["total_volumes"]
    
    df_prices = pd.DataFrame(prices, columns=["timestamp", "price"])
    df_marketcap = pd.DataFrame(market_caps, columns=["timestamp", "market_cap"])
    df_volume = pd.DataFrame(volumes, columns=["timestamp", "volume"])
    
    df = df_prices.merge(df_marketcap, on="timestamp")
    df = df.merge(df_volume, on="timestamp")
    df["date"] = pd.to_datetime(df["timestamp"], unit="ms")
    df = df[["date", "price", "market_cap", "volume"]]
    df = df.sort_values("date").reset_index(drop=True)
    
    return df

@st.cache_data(ttl=3600)  # Cache 1 jam
def load_data_from_api():
    """Load data langsung dari API"""
    try:
        with st.spinner('Fetching data from CoinGecko...'):
            raw_data = extract_bitcoin_data()
            df = transform_bitcoin_data(raw_data)
        return df
    except Exception as e:
        st.error(f"Error fetching from API: {e}")
        return pd.DataFrame()

# Panggil fungsi
df = load_data_from_api()

# Fungsi untuk menghitung moving average
def calculate_moving_average(df, window):
    return df['price'].rolling(window=window).mean()

# Load data
with st.spinner('Loading data...'):
    df = load_data()

# Cek apakah data kosong
if df.empty:
    st.error("No data available. Please check database connection.")
    st.stop()

# Header dengan gradient
st.markdown("""
    <div class="title">
        <h1>📊 Bitcoin Market Dashboard</h1>
        <p style="opacity: 0.9;">Real-time cryptocurrency market analysis</p>
    </div>
""", unsafe_allow_html=True)

# Sidebar untuk filter dan kontrol
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/4/46/Bitcoin.svg/1200px-Bitcoin.svg.png", 
             width=100)
    st.markdown("## ⚙️ Controls")
    
    # Date range filter
    min_date = df['date'].min().date()
    max_date = df['date'].max().date()
    
    date_range = st.date_input(
        "Select Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
    
    if len(date_range) == 2:
        start_date, end_date = date_range
        df_filtered = df[(df['date'].dt.date >= start_date) & 
                         (df['date'].dt.date <= end_date)]
    else:
        df_filtered = df
    
    # Moving average window
    ma_window = st.slider("Moving Average Window (days)", 7, 90, 30)
    
    # Chart theme
    theme = st.selectbox("Chart Theme", ["light", "dark"])
    
    st.markdown("---")
    st.markdown("### 📈 Key Statistics")
    st.markdown(f"**Data Points:** {len(df_filtered):,}")
    st.markdown(f"**Date Range:** {df_filtered['date'].min().date()} to {df_filtered['date'].max().date()}")
    
    # Download button
    csv = df_filtered.to_csv(index=False)
    st.download_button(
        label="📥 Download Data",
        data=csv,
        file_name=f"bitcoin_data_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )

# Main content
# Row 1: Key Metrics
st.markdown("## 📈 Market Overview")
col1, col2, col3, col4 = st.columns(4)

with col1:
    current_price = df_filtered['price'].iloc[-1]
    price_change = df_filtered['price'].iloc[-1] - df_filtered['price'].iloc[-2]
    price_change_pct = (price_change / df_filtered['price'].iloc[-2]) * 100
    st.metric(
        "Current Price",
        f"${current_price:,.2f}",
        f"{price_change:+,.2f} ({price_change_pct:+.2f}%)"
    )

with col2:
    avg_price = df_filtered['price'].mean()
    st.metric("Average Price (Period)", f"${avg_price:,.2f}")

with col3:
    highest_price = df_filtered['price'].max()
    highest_date = df_filtered.loc[df_filtered['price'].idxmax(), 'date'].date()
    st.metric("Highest Price", f"${highest_price:,.2f}", f"on {highest_date}")

with col4:
    lowest_price = df_filtered['price'].min()
    lowest_date = df_filtered.loc[df_filtered['price'].idxmin(), 'date'].date()
    st.metric("Lowest Price", f"${lowest_price:,.2f}", f"on {lowest_date}")

# Row 2: Price Chart with Moving Average
st.markdown("## 📊 Price Analysis")
fig = make_subplots(
    rows=2, cols=1,
    shared_xaxes=True,
    vertical_spacing=0.05,
    row_heights=[0.7, 0.3],
    subplot_titles=('Bitcoin Price with Moving Average', 'Trading Volume')
)

# Price line
fig.add_trace(
    go.Scatter(
        x=df_filtered['date'],
        y=df_filtered['price'],
        name='Price',
        line=dict(color='#FF9900', width=2),
        hovertemplate='Date: %{x}<br>Price: $%{y:,.2f}<extra></extra>'
    ),
    row=1, col=1
)

# Moving average
ma_values = calculate_moving_average(df_filtered, ma_window)
fig.add_trace(
    go.Scatter(
        x=df_filtered['date'],
        y=ma_values,
        name=f'{ma_window}-day MA',
        line=dict(color='#00CC96', width=2, dash='dash'),
        hovertemplate='Date: %{x}<br>MA: $%{y:,.2f}<extra></extra>'
    ),
    row=1, col=1
)

# Volume bars
fig.add_trace(
    go.Bar(
        x=df_filtered['date'],
        y=df_filtered['volume'],
        name='Volume',
        marker_color='#636EFA',
        opacity=0.7,
        hovertemplate='Date: %{x}<br>Volume: $%{y:,.0f}<extra></extra>'
    ),
    row=2, col=1
)

# Update layout
fig.update_layout(
    height=700,
    showlegend=True,
    hovermode='x unified',
    template='plotly_dark' if theme == 'dark' else 'plotly_white',
    title={
        'text': f"Bitcoin Price Analysis ({start_date} to {end_date})",
        'y':0.98,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'
    }
)

fig.update_xaxes(title_text="Date", row=2, col=1)
fig.update_yaxes(title_text="Price (USD)", row=1, col=1)
fig.update_yaxes(title_text="Volume (USD)", row=2, col=1)

st.plotly_chart(fig, use_container_width=True)

# Row 3: Additional Charts
st.markdown("## 📉 Advanced Analytics")
col1, col2 = st.columns(2)

with col1:
    # Market Cap Chart
    fig_mcap = px.area(
        df_filtered, 
        x='date', 
        y='market_cap',
        title='Market Capitalization',
        labels={'market_cap': 'Market Cap (USD)', 'date': 'Date'},
        template='plotly_dark' if theme == 'dark' else 'plotly_white'
    )
    fig_mcap.update_traces(line_color='#00CC96', fillcolor='rgba(0,204,150,0.3)')
    st.plotly_chart(fig_mcap, use_container_width=True)

with col2:
    # Price Distribution Histogram
    fig_hist = px.histogram(
        df_filtered, 
        x='price',
        nbins=30,
        title='Price Distribution',
        labels={'price': 'Price (USD)', 'count': 'Frequency'},
        template='plotly_dark' if theme == 'dark' else 'plotly_white'
    )
    fig_hist.update_traces(marker_color='#FF9900', marker_line_color='#FF9900')
    st.plotly_chart(fig_hist, use_container_width=True)

# Row 4: Statistics Table
st.markdown("## 📋 Detailed Statistics")
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### Descriptive Statistics")
    stats_df = df_filtered[['price', 'market_cap', 'volume']].describe()
    stats_df.index = ['Count', 'Mean', 'Std', 'Min', '25%', '50%', '75%', 'Max']
    st.dataframe(
        stats_df.style.format('${:,.2f}'),
        use_container_width=True
    )

with col2:
    st.markdown("### Recent Data")
    recent_df = df_filtered.tail(10)[['date', 'price', 'market_cap', 'volume']].copy()
    recent_df['date'] = recent_df['date'].dt.date
    recent_df.columns = ['Date', 'Price (USD)', 'Market Cap (USD)', 'Volume (USD)']
    st.dataframe(
        recent_df.style.format({
            'Price (USD)': '${:,.2f}',
            'Market Cap (USD)': '${:,.0f}',
            'Volume (USD)': '${:,.0f}'
        }),
        use_container_width=True
    )

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: gray; padding: 1rem;'>
        <p>Data source: CoinGecko API | Last updated: {}</p>
        <p>Built with Streamlit • PostgreSQL • Plotly</p>
    </div>
""".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")), unsafe_allow_html=True)

# Run with: streamlit run Dashboard.py
