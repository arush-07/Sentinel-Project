import streamlit as st
import pandas as pd
import time
import os

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Sentinel Command Center", layout="wide", page_icon="🛡️")

# --- CUSTOM STYLING ---
st.markdown("""
<style>
    .critical { background-color: #ff4b4b; padding: 5px; border-radius: 5px; color: white; }
    .medium { background-color: #ffa421; padding: 5px; border-radius: 5px; color: black; }
    .low { background-color: #21c354; padding: 5px; border-radius: 5px; color: black; }
    div.stMetric { background-color: #0E1117; border: 1px solid #303030; padding: 10px; border-radius: 10px; }
</style>
""", unsafe_allow_html=True)

# --- HEADER ---
c1, c2 = st.columns([1, 4])
with c1:
    st.image("https://cdn-icons-png.flaticon.com/512/1673/1673612.png", width=80) # Shield Icon
with c2:
    st.title("Sentinel: Autonomous Crisis Response Agent")
    st.caption("⚡ Powered by Pathway (Streaming Engine) & Gemini 2.5 (Agentic Brain)")

placeholder = st.empty()

def load_data():
    if not os.path.exists("output.csv"):
        return pd.DataFrame()
    try:
        df = pd.read_csv("output.csv")
        
        # Deduplicate
        if not df.empty and 'timestamp' in df.columns and 'report' in df.columns:
            df = df.drop_duplicates(subset=['timestamp', 'report'])
        
        # Parse AI Decision
        if not df.empty and 'ai_decision' in df.columns:
            split_data = df['ai_decision'].str.split('|', expand=True)
            if split_data.shape[1] >= 3:
                df['Severity'] = split_data[0].str.strip()
                df['Unit'] = split_data[1].str.strip()
                df['Plan'] = split_data[2].str.strip()
            else:
                df['Severity'] = "PROCESSING"
        
        return df
    except:
        return pd.DataFrame()

# --- MAIN LOOP ---
while True:
    df = load_data()
    
    with placeholder.container():
        if df.empty:
            st.info("📡 System Online. Waiting for live data stream...")
        else:
            # 1. METRICS ROW
            k1, k2, k3, k4 = st.columns(4)
            k1.metric("Total Events", len(df))
            
            crit_count = len(df[df['Severity'].str.contains("Critical", case=False, na=False)]) if 'Severity' in df.columns else 0
            k2.metric("CRITICAL ALERTS", crit_count, delta_color="inverse")
            
            last_update = df['timestamp'].iloc[-1] if 'timestamp' in df.columns else "--:--"
            k3.metric("Last Update", last_update)
            k4.metric("Agent Status", "ACTIVE 🟢")

            st.divider()

            # 2. MAP & DETAILS SPLIT
            col_map, col_table = st.columns([1, 1])
            
            with col_map:
                st.subheader("📍 Live Crisis Map")
                # Ensure we have coordinates for the map
                if 'latitude' in df.columns and 'longitude' in df.columns:
                    map_data = df[['latitude', 'longitude']].dropna()
                    st.map(map_data, zoom=12)
                else:
                    st.warning("Awaiting geospatial data...")

            with col_table:
                st.subheader("📝 Real-Time Decisions")
                # Show only key columns
                if 'Severity' in df.columns:
                    st.dataframe(
                        df[['timestamp', 'Severity', 'Unit', 'Plan']], 
                        hide_index=True, 
                        use_container_width=True,
                        height=300
                    )

            # 3. RAW FEED EXPANDER
            with st.expander("View Raw Incoming Reports"):
                st.dataframe(df, use_container_width=True)

    time.sleep(2)