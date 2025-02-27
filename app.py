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

# Add this near the top of your file, after the imports
if 'last_refresh' not in st.session_state:
    st.session_state.last_refresh = datetime.now()

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

# Add this before the try block
col1, col2 = st.columns([4, 1])
with col2:
    if st.button('🔄 Refresh'):
        st.session_state.last_refresh = datetime.now()
        st.experimental_rerun()

try:
    # Fetch data
    ticker = yf.Ticker(symbol)
    current_data = ticker.history(period='1d')
    historical_data = ticker.history(period='1mo')
    
    # Check if we have data
    if current_data.empty or historical_data.empty:
        st.error(f"No data available for {selected_commodity} at the moment. The market might be closed.")
    else:
        # Display current price
        current_price = current_data['Close'].iloc[-1]
        st.header(f"Current {selected_commodity} Price")
        st.subheader(f"${current_price:.2f}")
        
        # Calculate price change
        try:
            price_change = current_price - historical_data['Close'].iloc[-2]
            price_change_pct = (price_change / historical_data['Close'].iloc[-2]) * 100
            
            # Display price change with color
            if price_change >= 0:
                st.success(f"↗ ${price_change:.2f} ({price_change_pct:.2f}%)")
            else:
                st.error(f"↘ ${price_change:.2f} ({price_change_pct:.2f}%)")
        except:
            st.warning("Unable to calculate price change")
        
        # Display chart if we have enough data points
        if len(historical_data) > 0:
            st.subheader(f"{selected_commodity} Price - Last 30 Days")
            st.line_chart(historical_data['Close'])
        
        # Display additional information
        st.subheader("Additional Information")
        col1, col2 = st.columns(2)
        
        try:
            with col1:
                st.metric("Day's High", f"${historical_data['High'].iloc[-1]:.2f}")
                st.metric("Day's Low", f"${historical_data['Low'].iloc[-1]:.2f}")
            
            with col2:
                st.metric("Volume", f"{historical_data['Volume'].iloc[-1]:,.0f}")
                st.metric("Opening Price", f"${historical_data['Open'].iloc[-1]:.2f}")
        except:
            st.warning("Some market data is unavailable")

except Exception as e:
    st.error("Error fetching data. Please try again later.")
    st.exception(e)

# Add this after the try-except block
st.markdown(f"Last updated: {st.session_state.last_refresh.strftime('%Y-%m-%d %H:%M:%S')}")

# Add footer
st.markdown("---")
st.markdown("Data provided by Yahoo Finance") 
