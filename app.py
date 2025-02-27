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
st.title("Energy Commodity Prices")
st.markdown("Select a commodity to view its price and trends")

# Dictionary of commodities and their corresponding CSV files
#COMMODITIES = {
    #"E-mini Crude Oil": "pricedata/E-mini Crude Oil Futures Historical Data.csv",
    #"Gasoline RBOB": "pricedata/Gasoline RBOB Futures Historical Data.csv",
    #"Heating Oil": "pricedata/Heating Oil Futures Historical Data.csv"}

COMMODITIES = {
    "Dutch TTF Natural Gas Futures": "pricedata/Dutch TTF Natural Gas Futures Historical Data.csv",
    "London Gas Oil Futures": "pricedata/London Gas Oil Futures Historical Data.csv",
    "Micro Henry Hub Natural Gas Futures": "pricedata/Micro Henry Hub Natural Gas Futures Historical Data.csv",
    "Natural Gas Futures": "pricedata/Natural Gas Futures Historical Data.csv",
    "Brent Oil": "pricedata/Brent Oil Futures Historical Data.csv",
    "Crude Oil WTI": "pricedata/Crude Oil WTI Futures Historical Data.csv",
    "Carbon Emissions": "pricedata/Carbon Emissions Futures Historical Data.csv",
}
# Add this after the imports
COMMODITY_INFO = {
    "Brent Oil": {
        "Description": "Brent Crude is a major trading classification of sweet light crude oil that serves as a benchmark price for purchases of oil worldwide. It is extracted from the North Sea and comprises Brent Blend, Forties Blend, Oseberg and Ekofisk crudes.",
        "trading_hours": "Sunday-Friday: 23:00-22:00 GMT",
        "Trading": "Priced in USD per barrel. The standard contract size is 1,000 barrels. Driven by OPEC decisions, geopolitical risks, and global demand trends.",
        "Market": "Traded on ICE Futures Europe and NYMEX.",
    },
    "Carbon Emissions": {
        "Description": "Carbon Emissions futures represent the price of European Union Allowances (EUAs) under the EU Emissions Trading System (ETS). Each EUA allows companies to emit one ton of CO₂",
        "trading_hours": "Monday-Friday: 07:00-17:00 CET",
        "Trading": "Priced in EUR per metric ton of CO₂. The contract size is 1,000 EUAs (1,000 metric tons of CO₂). Driven by climate policies, carbon reduction targets, and market speculation.",
        "Market": "Traded on ICE Futures Europe and EEX",
    },
    "Crude Oil WTI": {
        "Description": "West Texas Intermediate (WTI) crude oil is a specific grade of crude oil and one of the main benchmark prices for purchases of oil worldwide. WTI is known as a light sweet oil because it contains around 0.24% sulfur.",
        "trading_hours": "Sunday-Friday: 18:00-17:00 EST",
        "Trading": "Priced in USD per barrel. The standard contract size is 1,000 barrels. Heavily influenced by US production, refining demand, and inventory reports.",
        "Market": "Traded on NYMEX (CME Group)",
    },
    "Dutch TTF Natural Gas Futures": {
        "Description": "The Title Transfer Facility (TTF) is a virtual trading point for natural gas in the Netherlands. It is the leading European benchmark for gas prices and one of the most liquid gas trading points in Europe.",
        "trading_hours": "Monday-Friday: 07:00-17:00 CET",
        "Trading": "Priced in USD per MMBtu. The standard contract size is 10,000 MMBtu. Highly influenced by seasonal demand, production levels, LNG exports, and storage reports.", 
        "Market": "Traded on NYMEX (CME Group)",
    },
    "London Gas Oil Futures": {
        "Description": "London Gas Oil (also known as diesel or heating oil) is a middle distillate oil used both as a diesel automotive fuel and heating fuel. It's the primary hedging tool for the middle of the oil barrel.",
        "trading_hours": "Monday-Friday: 01:00-23:00 GMT",
        "Trading": "Priced in US dollars per metric ton. The contract size is 100 metric tons. Often used for hedging by refiners, traders, and transportation companies.", 
        "Market": "Traded on ICE Futures Europe",
    },
    "Micro Henry Hub Natural Gas Futures": {
        "Description": "Micro Henry Hub Natural Gas futures are smaller-sized contracts that track natural gas prices at the Henry Hub in Louisiana, which is the primary price benchmark for natural gas futures in North America.",
        "trading_hours": "Sunday-Friday: 18:00-17:00 EST",
        "Trading": "Priced in USD per MMBtu (million British thermal units). The contract size is 2,500 MMBtu, which is 1/10th of the standard Henry Hub contract. More accessible for retail investors but still impacted by storage levels, weather, and production trends.", 
        "Market": "Traded on CME Group (NYMEX).",
    },
    "Natural Gas Futures": {
        "Description": "Henry Hub Natural Gas futures are standardized contracts for the physical delivery of natural gas. The contracts are based on delivery at the Henry Hub in Louisiana, the nexus of 16 intra- and interstate natural gas pipeline systems.",
        "trading_hours": "Sunday-Friday: 18:00-17:00 EST",
        "Trading": "Priced in USD per MMBtu. The standard contract size is 10,000 MMBtu. Highly influenced by seasonal demand, production levels, LNG exports, and storage reports.", 
        "Market": "Traded on NYMEX (CME Group)",
    },
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
        
# Display commodity information
st.subheader("Commodity Information")
if selected_commodity in COMMODITY_INFO:
    info = COMMODITY_INFO[selected_commodity]
    
    # Create tabs for different information categories
    tabs = st.tabs(["Overview", "Trading Details"])
    
    with tabs[0]:
        st.markdown("### Description")
        st.write(info["Description"])

# Add a divider
st.markdown("---")

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
