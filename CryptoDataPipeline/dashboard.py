import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

# --- Set Up the Page ---
st.set_page_config(page_title="Crypto Dashboard", layout="wide")
st.title("📊 Real-Time Crypto Prices Dashboard")

# --- Load Data from SQLite ---
@st.cache_data(ttl=60)
def load_data():
    conn = sqlite3.connect("data/crypto_data.db")
    df = pd.read_sql("SELECT * FROM crypto_prices", conn)
    conn.close()
    
    # Ensure we have a datetime column for trends
    if 'timestamp' not in df.columns:
        df['timestamp'] = pd.to_datetime('now')  # Add current time if no timestamp exists
    return df

df = load_data()

# Show available columns for debugging
st.write("Available columns:", df.columns.tolist())

# --- Show Raw Data ---
st.subheader("Raw Data")
st.dataframe(df)

# --- Interactive Price Chart ---
st.subheader("Price Trends")

# Let user choose which column to use as x-axis
x_axis = st.selectbox(
    "Choose time axis",
    options=[col for col in df.columns if 'date' in col.lower() or 'time' in col.lower()] or ['timestamp'],
    index=0
)

selected_coins = st.multiselect(
    "Select Cryptocurrencies", 
    df['name'].unique(), 
    default=["Bitcoin", "Ethereum"] if len(df['name'].unique()) > 1 else []
)

if selected_coins:
    filtered_df = df[df['name'].isin(selected_coins)]
    
    fig = px.line(
        filtered_df,
        x=x_axis,
        y="current_price",
        color="name",
        title="Price Over Time",
        labels={"current_price": "Price (USD)"}
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("Please select at least one cryptocurrency")

# --- Market Cap Bar Chart ---
st.subheader("Market Capitalization")
fig2 = px.bar(
    df.sort_values("market_cap", ascending=False).head(10),
    x="name",
    y="market_cap",
    title="Top 10 Cryptocurrencies by Market Cap"
)
st.plotly_chart(fig2, use_container_width=True)

# --- Price Change Visualization ---
st.subheader("24h Price Change (%)")

# Use a bar chart instead of heatmap if few coins
if len(df) > 5:
    fig3 = px.imshow(
        df.set_index('name')[['24h_change']],
        text_auto=True,
        color_continuous_scale="RdYlGn"
    )
else:
    fig3 = px.bar(
        df,
        x="name",
        y="24h_change",
        color="24h_change",
        color_continuous_scale="RdYlGn"
    )
st.plotly_chart(fig3, use_container_width=True)