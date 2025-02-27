import streamlit as st
import pandas as pd
from datetime import datetime
import os

# Set page config
st.set_page_config(
    page_title="Real-Time Commodity Prices",
    page_icon="📈",
    layout="wide"
)

# Initialize session state for refresh
if 'last_refresh' not in st.session_state:
    st.session_state.last_refresh = datetime.now()

# Title and description
st.title("Commodity Prices")
st.markdown("Select a commodity to view its price and trends")

# Dictionary of commodities and their corresponding CSV files
#COMMODITIES = {
    #"Brent Oil": "pricedata/Brent Oil Futures Historical Data.csv",
    #"Carbon Emissions": "pricedata/Carbon Emissions Futures Historical Data.csv",
    #"Crude Oil WTI": "pricedata/Crude Oil WTI Futures Historical Data.csv",
    #"E-mini Crude Oil": "pricedata/E-mini Crude Oil Futures Historical Data.csv",
    #"Gasoline RBOB": "pricedata/Gasoline RBOB Futures Historical Data.csv",
    #"Heating Oil": "pricedata/Heating Oil Futures Historical Data.csv"}

COMMODITIES = {
    "Dutch TTF Natural Gas Futures": "pricedata/Dutch TTF Natural Gas Futures Historical Data.csv",
    "London Gas Oil Futures": "pricedata/London Gas Oil Futures Historical Data.csv",
    "Micro Henry Hub Natural Gas Futures": "pricedata/Micro Henry Hub Natural Gas Futures Historical Data.csv",
    "Natural Gas Futures": "pricedata/Natural Gas Futures Historical Data.csv"
}
# Create the dropdown
selected_commodity = st.selectbox(
    "Choose a commodity",
    list(COMMODITIES.keys())
)

# Add refresh button
col1, col2 = st.columns([4, 1])
with col2:
    if st.button('🔄 Refresh'):
        st.session_state.last_refresh = datetime.now()
        st.experimental_rerun()

try:
    # Read CSV file
    csv_path = COMMODITIES[selected_commodity]
    df = pd.read_csv(csv_path)
    
    # Convert Date column to datetime
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Sort by date
    df = df.sort_values('Date')
    
    # Clean up the Price column (remove commas and convert to float)
    df['Price'] = df['Price'].replace({',': ''}, regex=True).astype(float)
    
    if not df.empty:
        # Display current price (most recent data)
        current_price = df['Price'].iloc[-1]
        st.header(f"Latest {selected_commodity} Price")
        st.subheader(f"${current_price:.2f}")
        
        # Calculate price change
        try:
            price_change = current_price - df['Price'].iloc[-2]
            price_change_pct = (price_change / df['Price'].iloc[-2]) * 100
            
            # Display price change with color
            if price_change >= 0:
                st.success(f"↗ ${price_change:.2f} ({price_change_pct:.2f}%)")
            else:
                st.error(f"↘ ${price_change:.2f} ({price_change_pct:.2f}%)")
        except:
            st.warning("Unable to calculate price change")
        
        # Display chart
        st.subheader(f"{selected_commodity} Price History")
        st.line_chart(df.set_index('Date')['Price'])
        
        # Display additional information
        st.subheader("Latest Trading Information")
        col1, col2 = st.columns(2)
    
        # Add date range selector
        st.subheader("Date Range Selection")
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Start Date", df['Date'].min())
        with col2:
            end_date = st.date_input("End Date", df['Date'].max())
        
        # Filter data based on date range
        mask = (df['Date'].dt.date >= start_date) & (df['Date'].dt.date <= end_date)
        filtered_df = df.loc[mask]
        
except Exception as e:
    st.error("Error loading data. Please try again later.")
    st.exception(e)

# Display last update time
st.markdown(f"Last updated: {st.session_state.last_refresh.strftime('%Y-%m-%d %H:%M:%S')}")

# Add footer
st.markdown("---")
st.markdown("Data from local CSV files") 
