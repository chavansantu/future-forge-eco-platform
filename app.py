import streamlit as st
import pandas as pd

# --- PAGE CONFIG ---
st.set_page_config(page_title="Future Forge Platform", layout="wide")

# --- GLOBAL WASTE DATABASE ---
global_data = {
    "usa": {"daily": "2.22 kg", "monthly": "66.6 kg", "annual": "811 kg"},
    "india": {"daily": "0.45 kg", "monthly": "13.5 kg", "annual": "164 kg"},
    "germany": {"daily": "1.30 kg", "monthly": "39.0 kg", "annual": "475 kg"},
    "japan": {"daily": "1.00 kg", "monthly": "30.0 kg", "annual": "365 kg"},
    "global_avg": {"daily": "0.88 kg", "monthly": "26.4 kg", "annual": "321 kg"}
}

# --- SEARCH ENGINE DATA ---
waste_types = {
    "organic": "Organic Waste: 44% of global volume. Strategy: Composting/Biogas.",
    "plastic": "Plastic Waste: 12% of global volume. Strategy: Advanced Sorting/Recycling.",
    "paper": "Paper/Cardboard: 17% of global volume. Strategy: Pulping/Recycling.",
    "e-waste": "E-waste: Rapidly growing. Strategy: Specialized Hazardous Recovery."
}

st.title("🚀 Future Forge: Decision Intelligence Platform")

# --- ANALYTICS ENGINE ---
st.subheader("📊 Query Global Waste per Country")
country_input = st.selectbox("Select a country/region to analyze:", ["Global_Avg", "USA", "India", "Germany", "Japan"])

# Fetch data based on selection
data = global_data[country_input.lower()]

col1, col2, col3 = st.columns(3)
col1.metric(f"{country_input} Daily", data['daily'])
col2.metric(f"{country_input} Monthly", data['monthly'])
col3.metric(f"{country_input} Annual", data['annual'])

st.divider()

# --- SEARCH ENGINE FOR TYPES ---
st.subheader("🔍 Waste Composition & Strategy Lookup")
query = st.text_input("Search waste types (e.g., 'Organic', 'Plastic', 'E-waste'):")

if query:
    found = False
    for key in waste_types:
        if key in query.lower():
            st.success(waste_types[key])
            found = True
            break
    if not found and query:
        st.info("Try searching 'Organic', 'Plastic', 'Paper', or 'E-waste'.")

st.divider()

# --- MOCK DATA ENGINE ---
@st.cache_data
def load_data():
    return pd.DataFrame({
        'location_id': range(1, 11),
        'waste_density': [0.2, 0.5, 0.8, 0.3, 0.9, 0.4, 0.6, 0.2, 0.7, 0.5],
        'status': ['Clear', 'Anomaly', 'Clear', 'Urgent', 'Clear', 'Anomaly', 'Urgent', 'Clear', 'Clear', 'Anomaly']
    })

df = load_data()
st.write("### Real-time Municipal Anomaly Monitor")
st.bar_chart(df.set_index('location_id')['waste_density'])
st.bar_chart(df.set_index('location_id')['waste_density'])

st.caption("Data Source: Compiled Global Municipal Solid Waste Statistics (2026).")
