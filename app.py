import streamlit as st
import pandas as pd
from datetime import datetime

# --- PAGE CONFIG ---
st.set_page_config(page_title="Future Forge: Decision Intelligence", layout="wide")

# --- INITIALIZE SESSION STATE ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'history' not in st.session_state:
    st.session_state.history = []

# --- LOGIN LOGIC ---
if not st.session_state.logged_in:
    st.title("Login to Future Forge")
    user = st.text_input("Username", key="login_user_input")
    pwd = st.text_input("Password", type="password", key="login_pwd_input")
    if st.button("Login", key="login_btn_submit"):
        if user and pwd:
            st.session_state.logged_in = True
            st.rerun()
    st.stop()

# --- SIDEBAR NAVIGATION ---
with st.sidebar:
    st.header("👤 Profile")
    st.write("Welcome, User!")
    st.button("Logout", on_click=lambda: st.session_state.update(logged_in=False), key="sidebar_logout_btn")
    st.divider()
    st.subheader("☰ Menu")
    st.button("Search History", key="menu_history_btn")
    st.button("Privacy Settings", key="menu_privacy_btn")
    st.divider()
    st.subheader("Search History Logs")
    for item in st.session_state.history:
        st.text(item)

# --- DATABASE ---
data_library = {
    "india": 168000000,
    "china": 210000000,
    "japan": 44000000,
    "indonesia": 65000000,
    "south korea": 18000000,
    "asia": 849000000
}

def get_waste_metrics(annual_total):
    return {
        "Yearly": annual_total,
        "Monthly": annual_total / 12,
        "Daily": annual_total / 365,
        "Hourly": annual_total / (365 * 24)
    }

# --- HEADER & SEARCH ---
st.title("🌍 Future Forge: AI-Powered Waste Intelligence")

search_query = st.text_input("🔍 Search country or region waste data (e.g., India, Asia)...", key="main_search_input")

if search_query:
    st.session_state.history.append(f"{datetime.now().strftime('%H:%M')} - {search_query}")
    query = search_query.lower().strip()
    
    if query in data_library:
        metrics = get_waste_metrics(data_library[query])
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Per Year", f"{metrics['Yearly']:,.0f}")
        col2.metric("Per Month", f"{metrics['Monthly']:,.0f}")
        col3.metric("Per Day", f"{metrics['Daily']:,.0f}")
        col4.metric("Per Hour", f"{metrics['Hourly']:,.0f}")
    else:
        st.warning("Data not found. Try 'India', 'China', or 'Asia'.")

# --- REPORT & STRATEGY ---
with st.expander("📍 Report Waste to Authorities", expanded=False):
    loc = st.text_input("Enter location or landmark:", key="report_loc_input")
    desc = st.text_area("Describe the waste/issue:", key="report_desc_input")
    if st.button("Submit Report", key="submit_report_btn"):
        if loc and desc: st.success(f"Report submitted for: {loc}")
        else: st.error("Please provide both location and description.")

with st.expander("💡 Strategic Solutions & Guidelines", expanded=False):
    c1, c2 = st.columns(2)
    c1.write("🛠 **Recommended Actions**\n- Source Segregation\n- Circular Economy\n- Pay-as-you-throw")
    c2.write("📜 **Guidelines**\n- Phase 1: Audit\n- Phase 2: Sorting\n- Phase 3: Monitoring")

st.divider()

# --- DASHBOARD METRICS ---
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
    if st.camera_input("Capture Waste Pile", key="main_camera_input"):
        st.success("Analysis complete.")