import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import date, timedelta

# Set page config
st.set_page_config(page_title="Stock Insight Hub", layout="wide", initial_sidebar_state="expanded")

# Custom CSS to enhance the UI
st.markdown("""
<style>
    .reportview-container {
        background: linear-gradient(to right, #FFFFFF, #F0F8FF);
    }
    .sidebar .sidebar-content {
        background: linear-gradient(to bottom, #4B0082, #8A2BE2);
    }
    .Widget>label {
        color: #FFFFFF;
        font-family: 'Trebuchet MS', sans-serif;
    }
    .stButton>button {
        color: #4B0082;
        background-color: #FFD700;
        border-radius: 20px;
    }
    .stTextInput>div>div>input {
        color: #4B0082;
    }
    h1, h2, h3 {
        color: #4B0082;
    }
</style>
""", unsafe_allow_html=True)

# Title and description
st.title("✨ Stock Insight Hub ✨")
st.markdown("Dive into the world of stocks with our interactive analysis tool!")

# Sidebar
st.sidebar.image("https://img.icons8.com/nolan/64/stocks.png", width=100)
st.sidebar.title("Control Panel")

# Get user input
ticker = st.sidebar.text_input("Enter Stock Ticker (e.g., AAPL, GOOGL)", "AAPL")
start_date = st.sidebar.date_input("Start Date", date.today() - timedelta(days=365))
end_date = st.sidebar.date_input("End Date", date.today())

# Fetch data
@st.cache_data
def load_data(ticker, start, end):
    data = yf.download(ticker, start=start, end=end)
    data.reset_index(inplace=True)
    return data

data = load_data(ticker, start_date, end_date)

# Main content
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📈 Stock Price Journey")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name="Close Price", line=dict(color="#4B0082", width=2)))
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Open'], name="Open Price", line=dict(color="#FFD700", width=2)))
    fig.layout.update(
        title_text=f"{ticker} Stock Price Odyssey", 
        xaxis_rangeslider_visible=True,
        plot_bgcolor="rgba(0,0,0,0)",
        yaxis_title="Price (USD)",
        xaxis_title="Date",
        legend_title="Price Type",
        font=dict(family="Trebuchet MS, sans-serif", size=12, color="#4B0082")
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("🔍 Quick Stats")
    latest_price = data['Close'].iloc[-1]
    price_change = data['Close'].iloc[-1] - data['Close'].iloc[0]
    percent_change = (price_change / data['Close'].iloc[0]) * 100

    st.metric("Latest Magic Number", f"${latest_price:.2f}")
    st.metric("Price Spell", f"${price_change:.2f}", f"{percent_change:.2f}%")
    
    # Volume Analysis
    avg_volume = data['Volume'].mean()
    max_volume = data['Volume'].max()
    st.metric("Average Daily Trades", f"{avg_volume:.0f}")
    st.metric("Busiest Day Trades", f"{max_volume:.0f}")

# Moving Averages
st.subheader("🌊 Riding the Waves: Moving Averages")
data['MA50'] = data['Close'].rolling(window=50).mean()
data['MA200'] = data['Close'].rolling(window=200).mean()

fig_ma = go.Figure()
fig_ma.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name="Close Price", line=dict(color="#4B0082", width=2)))
fig_ma.add_trace(go.Scatter(x=data['Date'], y=data['MA50'], name="50-day MA", line=dict(color="#FFD700", width=2)))
fig_ma.add_trace(go.Scatter(x=data['Date'], y=data['MA200'], name="200-day MA", line=dict(color="#00CED1", width=2)))
fig_ma.layout.update(
    title_text=f"{ticker} Price with Trend Lines", 
    xaxis_rangeslider_visible=True,
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis_title="Price (USD)",
    xaxis_title="Date",
    legend_title="Indicators",
    font=dict(family="Trebuchet MS, sans-serif", size=12, color="#4B0082")
)
st.plotly_chart(fig_ma, use_container_width=True)

# Candlestick Chart
st.subheader("🕯️ Candlestick Enigma")
fig_candle = go.Figure(data=[go.Candlestick(x=data['Date'],
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                close=data['Close'])])
fig_candle.layout.update(
    title_text=f"{ticker} Candlestick Chart", 
    xaxis_rangeslider_visible=True,
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis_title="Price (USD)",
    xaxis_title="Date",
    font=dict(family="Trebuchet MS, sans-serif", size=12, color="#4B0082")
)
st.plotly_chart(fig_candle, use_container_width=True)

# Correlation Matrix
st.subheader("🔗 The Connection Web")
corr_matrix = data[['Open', 'High', 'Low', 'Close', 'Volume']].corr()

fig_heatmap = px.imshow(corr_matrix, 
                        labels=dict(color="Correlation"),
                        x=corr_matrix.columns,
                        y=corr_matrix.index,
                        color_continuous_scale="Viridis")
fig_heatmap.update_layout(
    title="Stock Attributes Correlation Heatmap",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Trebuchet MS, sans-serif", size=12, color="#4B0082")
)
st.plotly_chart(fig_heatmap, use_container_width=True)

# Volume Analysis
st.subheader("📊 Volume Ventures")
fig_volume = go.Figure()
fig_volume.add_trace(go.Bar(x=data['Date'], y=data['Volume'], name="Volume", marker_color="#4B0082"))
fig_volume.layout.update(
    title_text=f"{ticker} Trading Volume Over Time", 
    xaxis_rangeslider_visible=True,
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis_title="Volume",
    xaxis_title="Date",
    font=dict(family="Trebuchet MS, sans-serif", size=12, color="#4B0082")
)
st.plotly_chart(fig_volume, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("Created with ❤️ by Stock Insight Hub")
st.markdown("Data provided by Yahoo Finance")