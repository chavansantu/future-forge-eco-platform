import streamlit as st
import pandas as pd
import streamlit as st
from datetime import datetime

# Initialize Session State for Login and History
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'history' not in st.session_state:
    st.session_state.history = []

# --- Login Logic ---
if not st.session_state.logged_in:
    st.title("Login to Future Forge")
    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")
    if st.button("Login"):
        if user and pwd:  # Add your authentication logic here
            st.session_state.logged_in = True
            st.rerun()
    st.stop() # Stops the script if not logged in

# --- Dashboard Layout (Only visible if logged_in is True) ---
st.sidebar.button("Logout", on_click=lambda: st.session_state.update(logged_in=False))
st.sidebar.subheader("Search History")
for item in st.session_state.history:
    st.sidebar.text(item)

# Your existing Search Bar logic
query = st.text_input("Search waste data...")
if query:
    st.session_state.history.append(f"{datetime.now().strftime('%H:%M')} - {query}")
# --- PAGE CONFIG ---
st.set_page_config(page_title="Future Forge: Decision Intelligence", layout="wide")

# --- SIDEBAR: NAVIGATION ---
with st.sidebar:
    st.header("👤 Profile")
    st.write("Welcome, User!")
    st.divider()
    st.subheader("☰ Menu")
    st.button("Search History")
    st.button("Privacy Settings")
    st.divider()
    st.button("Login")
    st.button("Logout")
    st.caption("Future Forge Platform v1.0")

# --- DATABASE (Detailed & Structured) ---
data_library = {
    "india": "### 🇮🇳 India\n**Annual Waste Production:** ~168 Million Tonnes/Year\n**Waste Sources:** Household, Commercial, Industrial\n**Primary Waste Type:** High organic/wet waste (50-60%), moisture-rich.\n**Strategy:** Decentralized composting & informal sector integration.",
    "china": "### 🇨🇳 China\n**Annual Waste Production:** ~210 Million Tonnes/Year\n**Waste Sources:** Heavy Industrial, Commercial, Residential\n**Primary Waste Type:** Food waste, increasing packaging plastics, paper.\n**Strategy:** Large-scale waste-to-energy incineration.",
    "japan": "### 🇯🇵 Japan\n**Annual Waste Production:** ~44 Million Tonnes/Year\n**Waste Sources:** Industrial, Commercial, Household\n**Primary Waste Type:** Paper, cardboard, and plastics.\n**Strategy:** Stringent household sorting and thermal treatment.",
    "indonesia": "### 🇮🇩 Indonesia\n**Annual Waste Production:** ~65 Million Tonnes/Year\n**Waste Sources:** Household and Commercial\n**Primary Waste Type:** Organic (Food) and mixed plastics.\n**Strategy:** Community-based 'Waste Banks' and marine plastic collection.",
    "south korea": "### 🇰🇷 South Korea\n**Annual Waste Production:** ~18 Million Tonnes/Year\n**Waste Sources:** Commercial and Household\n**Primary Waste Type:** High food waste content.\n**Strategy:** Volume-based waste fees (pay-by-weight) and mandatory recycling.",
    "usa": "### 🇺🇸 United States\n**Annual Waste Production:** ~265 Million Tonnes/Year\n**Waste Sources:** Industrial, Commercial, Residential\n**Primary Waste Type:** Paper, plastics, metals, and food waste.\n**Strategy:** Landfill gas-to-energy and voluntary recycling programs.",
    "asia": """### 🌏 Asia-Pacific Regional Overview
**Total Regional Waste:** ~849 Million Tonnes/Year  
**Key Regional Sources:** Rapidly urbanizing Residential & Industrial sectors.  
**Regional Waste Profile:** Predominantly organic with rising plastic footprint.  
*Search for a specific country name (e.g., 'India') for a detailed breakdown.*"""
}

# --- HEADER ---
st.title("🌍 Future Forge: AI-Powered Waste Intelligence")

# --- SEARCH BAR (Integrated Asia logic) ---
search_input = st.text_input("🔍 Search Platform...", placeholder="e.g., 'India', 'Asia'")
# ... existing imports and layout code ...

# 1. SEARCH BAR AT THE TOP
search_query = st.text_input("🔍 Search country or region waste data...", "")

# --- INSERT NEW CODE HERE ---
def get_waste_metrics(query):
    # Base data for India
    daily_waste = 165000 
    hourly_waste = daily_waste / 24
    
    # You can customize this if the query is a specific region
    return daily_waste, hourly_waste

if search_query:
    d, h = get_waste_metrics(search_query)
    col1, col2 = st.columns(2)
    col1.metric("Waste per Day", f"{d:,.0f} Tonnes")
    col2.metric("Waste per Hour", f"{h:,.0f} Tonnes")
# --- END OF INSERTION ---

# 2. OVERVIEW & LOCATION (Your previously added code)
st.subheader("📍 Regional Overview & Location")
# ... (rest of your existing code follows here)
if search_input:
    query = search_input.lower().strip()
    found = False
    
    # 1. Check for Asia: Show Summary and List
    if "asia" in query:
        st.success(data_library["asia"])
        st.write("---")
        st.write("### 🌏 Countries included in our Dataset:")
        for country in ["india", "china", "japan", "indonesia", "south korea"]:
            st.write(f"- {country.upper()}")
        found = True
    
    # 2. Check for specific country (Exact Match)
    elif query in data_library:
        st.success(data_library[query])
        found = True
        
    # 3. Partial Match Fallback
    else:
        for keyword, response in data_library.items():
            if keyword in query:
                st.success(response)
                found = True
                break
                
    if not found:
        st.warning("Data not found. Try 'Asia' or specific country names (e.g., India, China).")

# --- REPORT & STRATEGY ---
with st.expander("📍 Report Waste to Authorities", expanded=False):
    loc = st.text_input("Enter location or landmark:")
    desc = st.text_area("Describe the waste/issue:")
    if st.button("Submit Report"):
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
    if st.camera_input("Capture Waste Pile"):
        st.success("Analysis complete.")