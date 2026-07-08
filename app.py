import streamlit as st
import pandas as pd
from datetime import datetime

# --- PAGE CONFIG ---
st.set_page_config(page_title="Future Forge: Decision Intelligence", layout="wide")

# --- INITIALIZE SESSION STATE ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'history' not in st.session_state: st.session_state.history = []

# --- LOGIN LOGIC ---
if not st.session_state.logged_in:
    st.title("Login to Future Forge")
    user = st.text_input("Username", key="login_user")
    pwd = st.text_input("Password", type="password", key="login_pass")
    if st.button("Login", key="btn_login_submit"):
        if user and pwd:
            st.session_state.logged_in = True
            st.rerun()
    st.stop()

# --- DATABASE ---
data_library = {
    "india": 170000, # Tonnes per day
    "china": 210000,
    "japan": 44000,
    "indonesia": 65000,
    "south korea": 18000,
    "asia": 849000
}

def get_waste_metrics(daily_total):
    return {
        "Yearly": daily_total * 365,
        "Monthly": daily_total * 30,
        "Daily": daily_total,
        "Hourly": daily_total / 24
    }

# --- SIDEBAR ---
with st.sidebar:
    st.header("👤 Profile")
    st.button("Logout", on_click=lambda: st.session_state.update(logged_in=False), key="btn_out")
    st.subheader("☰ Search History")
    for item in st.session_state.history: st.text(item)

# --- HEADER & SEARCH ---
st.title("🌍 Future Forge: AI-Powered Waste Intelligence")

search_query = st.text_input("🔍 Search country or region waste data...", key="main_search")

if search_query:
    st.session_state.history.append(f"{datetime.now().strftime('%H:%M')} - {search_query}")
    query = search_query.lower().strip()
    
    found_key = next((k for k in data_library if k in query), None)
            
    if found_key:
        metrics = get_waste_metrics(data_library[found_key])
        
        st.subheader(f"📊 Waste Insights for {found_key.upper()}")
        
        # Table output
        df_metrics = pd.DataFrame({
            "Timeframe": ["Yearly", "Monthly", "Daily", "Hourly"],
            "Waste Amount (Tonnes)": [f"{metrics['Yearly']:,.0f}", f"{metrics['Monthly']:,.0f}", f"{metrics['Daily']:,.0f}", f"{metrics['Hourly']:,.0f}"]
        })
        st.table(df_metrics)
        
        # Bulleted points
        st.write("##### Key Facts")
        st.markdown(f"""
        * **Current Status**: {found_key.capitalize()} generates roughly {data_library[found_key]:,.0f} tonnes of waste daily.
        * **Management**: New 2026 regulations now mandate four-stream segregation (Wet, Dry, Sanitary, Special-care) at the source.
        * **Accountability**: The 'Polluter Pays' principle is now enforced through environmental compensation for non-compliance.
        """)
    else:
        st.warning("Data not found. Try 'India', 'China', or 'Asia'.")

# --- REMAINING DASHBOARD SECTIONS ---
st.subheader("📍 Regional Overview & Location")
with st.expander("📍 Report Waste to Authorities", expanded=False):
    loc = st.text_input("Enter location:", key="rep_loc")
    desc = st.text_area("Describe issue:", key="rep_desc")
    if st.button("Submit Report", key="btn_rep"):
        st.success(f"Report submitted for: {loc}")

m1, m2, m3 = st.columns(3)
m1.metric("Annual Global Waste", "2.56B Tonnes")
m2.metric("Global Uncollected", "29%")
m3.metric("Plastic Composition", "12%")

col1, col2 = st.columns([2, 1])
with col1:
    st.write("### 📊 Global Waste Composition")
    st.bar_chart(pd.DataFrame({'Percentage': [44, 17, 12, 5, 4]}, index=['Organics', 'Paper', 'Plastic', 'Glass', 'Metal']))
with col2:
    st.write("### 📸 AI Vision Analysis")
    if st.camera_input("Capture Waste Pile", key="cam"):
        st.success("Analysis complete.")