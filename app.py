pip install streamlit yfinance pandas

import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

# Set page config
st.set_page_config(
    page_title="Real-Time Commodity Prices",
    page_icon="📈",
    layout="wide"
)

# Title and description
st.title("Real-Time Commodity Prices")
st.markdown("Select a commodity to view its current price and recent trends")

# Dictionary of common commodities and their symbols
COMMODITIES = {
    "Gold": "GC=F",
    "Silver": "SI=F",
    "Crude Oil": "CL=F",
    "Natural Gas": "NG=F",
    "Copper": "HG=F",
    "Platinum": "PL=F",
    "Corn": "ZC=F",
    "Wheat": "ZW=F"
}

# Create the dropdown
selected_commodity = st.selectbox(
    "Choose a commodity",
    list(COMMODITIES.keys())
)

# Get the symbol for the selected commodity
symbol = COMMODITIES[selected_commodity]

try:
    # Fetch data
    ticker = yf.Ticker(symbol)
    current_data = ticker.history(period='1d')
    historical_data = ticker.history(period='1mo')
    
    # Display current price
    current_price = current_data['Close'].iloc[-1]
    st.header(f"Current {selected_commodity} Price")
    st.subheader(f"${current_price:.2f}")
    
    # Calculate price change
    price_change = current_price - historical_data['Close'].iloc[-2]
    price_change_pct = (price_change / historical_data['Close'].iloc[-2]) * 100
    
    # Display price change with color
    if price_change >= 0:
        st.success(f"↗ ${price_change:.2f} ({price_change_pct:.2f}%)")
    else:
        st.error(f"↘ ${price_change:.2f} ({price_change_pct:.2f}%)")
    
    # Display chart
    st.subheader(f"{selected_commodity} Price - Last 30 Days")
    st.line_chart(historical_data['Close'])
    
    # Display additional information
    st.subheader("Additional Information")
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Day's High", f"${historical_data['High'].iloc[-1]:.2f}")
        st.metric("Day's Low", f"${historical_data['Low'].iloc[-1]:.2f}")
    
    with col2:
        st.metric("Volume", f"{historical_data['Volume'].iloc[-1]:,.0f}")
        st.metric("Opening Price", f"${historical_data['Open'].iloc[-1]:.2f}")

except Exception as e:
    st.error("Error fetching data. Please try again later.")
    st.exception(e)

# Add footer
st.markdown("---")
st.markdown("Data provided by Yahoo Finance") 
