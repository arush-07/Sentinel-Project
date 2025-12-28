import streamlit as st
import pandas as pd
import time
import os

st.set_page_config(page_title="Sentinel Command Center", layout="wide", page_icon="🛡️")

st.markdown("""
<style>
    div.stMetric { background-color: #0E1117; border: 1px solid #303030; padding: 10px; border-radius: 10px; }
</style>
""", unsafe_allow_html=True)

st.title("🛡️ Sentinel: Autonomous Crisis Response Agent")
st.caption("⚡ Powered by Pathway & Gemini 2.5")

placeholder = st.empty()

def load_data():
    if not os.path.exists("output.csv"):
        return pd.DataFrame()
    try:
        df = pd.read_csv("output.csv")
        
        # Remove duplicates
        if not df.empty and 'timestamp' in df.columns and 'report' in df.columns:
            df = df.drop_duplicates(subset=['timestamp', 'report'])
            
        # Parse AI Decision
        if not df.empty and 'ai_decision' in df.columns:
            split_data = df['ai_decision'].str.split('|', expand=True)
            if split_data.shape[1] >= 3:
                df['Severity'] = split_data[0]
                df['Unit'] = split_data[1]
                df['Plan'] = split_data[2]
            else:
                df['Severity'] = "PROCESSING"
        return df
    except:
        return pd.DataFrame()

while True:
    df = load_data()
    with placeholder.container():
        # Metrics
        k1, k2, k3 = st.columns(3)
        k1.metric("Total Events", len(df))
        
        crit_count = len(df[df['Severity'].str.contains("Critical", case=False, na=False)]) if 'Severity' in df.columns else 0
        k2.metric("CRITICAL ALERTS", crit_count)
        k3.metric("System Status", "ONLINE 🟢")

        st.divider()

        # Map and Table Layout
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("📍 Live Crisis Map")
            if 'latitude' in df.columns and 'longitude' in df.columns:
                st.map(df[['latitude', 'longitude']].dropna())
            else:
                st.info("Waiting for GPS data...")

        with col2:
            st.subheader("📝 Live Decisions")
            if 'Severity' in df.columns:
                st.dataframe(df[['timestamp', 'Severity', 'Unit', 'Plan']], hide_index=True)
    
    time.sleep(2)