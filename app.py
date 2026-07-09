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
    "india": 185000, 
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

# --- HEADER ---
st.markdown("""
    <div style="text-align: center; padding: 20px; background: linear-gradient(90deg, #1e3c72 0%, #2a5298 50%, #4facfe 100%); border-radius: 15px;">
        <h1 style="color: white; font-family: sans-serif; margin: 0;">🌍 Future Forge</h1>
        <p style="color: #e0e0e0; font-family: sans-serif; font-size: 1.2rem; margin: 5px 0 0 0;">
            AI-Powered Waste Intelligence
        </p>
    </div>
    <br>
""", unsafe_allow_html=True)

# --- SEARCH LOGIC ---
search_query = st.text_input("🔍 Search country or region waste data...", key="main_search")

if search_query:
    st.session_state.history.append(f"{datetime.now().strftime('%H:%M')} - {search_query}")
    query = search_query.lower().strip()
    found_key = next((k for k in data_library if k in query), None)
            
    if found_key:
        metrics = get_waste_metrics(data_library[found_key])
        st.subheader(f"📊 Waste Insights for {found_key.upper()}")
        
        df_metrics = pd.DataFrame({
            "Timeframe": ["Yearly", "Monthly", "Daily", "Hourly"],
            "Waste Amount (Tonnes)": [f"{metrics['Yearly']:,.0f}", f"{metrics['Monthly']:,.0f}", f"{metrics['Daily']:,.0f}", f"{metrics['Hourly']:,.0f}"]
        })
        st.table(df_metrics)
        
        if found_key == "india":
            st.markdown("""India generates about 1.85 lakh tonnes (185,000 tonnes) of solid waste. Over a single day, this equals about 132 grams of trash per person across its 1.4 billion population. Millions of tonnes end up in landfills yearly, as much of it is uncollected or untreated.
            
            **Check details for your specific city:**
            * **Bengaluru**: The tech capital creates around 5,000 to 6,000 tonnes of solid waste every day.
            * **Delhi**: The capital generates roughly 11,862 tonnes of fresh waste daily.
            
            If you want to know about your specific city, let me know! I can tell you:
            * Your city's daily waste total
            * How much of it gets recycled vs. dumped
            * Tips on home waste segregation""")
        else:
            st.markdown(f"**{found_key.capitalize()}** generates approximately {data_library[found_key]:,.0f} tonnes of solid waste daily. Significant portions remain uncollected or untreated, requiring urgent adoption of circular economy principles.")
    else:
        st.subheader("🌍 Global Waste Intelligence")
        st.markdown(f"""The world generates approximately 7 million tonnes of municipal solid waste daily. 
        If you are looking for specific national stats, please try searching 'India', 'China', or 'Asia'. 
        
        Let me know your city or state for localized data!""")

# --- TABS DASHBOARD ---
st.write("---")
tab1, tab2, tab3, tab4 = st.tabs(["🖼️ Images", "🌐 Forums", "🎥 Videos", "🛠️ Tools"])

with tab1:
    st.write("### 🏭 Major Global Waste Producers")
    image_urls = [
        "https://images.unsplash.com/photo-1506744038136-46273834b3fb",
        "https://images.unsplash.com/photo-1586016413664-56430335e38d",
        "https://images.unsplash.com/photo-1473341617437-09fed1adc577"
    ]
    captions = [
        "Steel Industry: Slag & furnace dust.",
        "Paper Mills: Sludge & chemical waste.",
        "Petrochemical: Chemical solvents."
    ]
    st.image(image_urls, caption=captions, width=300)

with tab2:
    st.markdown("- [UNEP Zero Waste](https://www.un.org/observances/zero-waste-day)\n- [World Bank Waste Data](https://www.worldbank.org/en/publication/what-a-waste)")

with tab3:
    st.video("https://www.youtube.com/watch?v=-wROiVYM44U")

with tab4:
    st.info("Solutions: Four-stream segregation, Waste-to-Energy (WTE), and Biological Reprocessing.")

# --- REMAINING SECTIONS ---
st.subheader("📍 Report Waste")
with st.expander("📍 Report Waste to Authorities"):
    loc = st.text_input("Enter location:", key="rep_loc")
    if st.button("Submit Report", key="btn_rep"): st.success(f"Report submitted for: {loc}")

# --- SIDE-BY-SIDE CHART AND CAMERA ---
col_chart, col_cam = st.columns(2)

with col_chart:
    st.write("### 📊 Global Waste Composition")
    st.metric("Annual Global Waste", "2.56B Tonnes")
    st.bar_chart(pd.DataFrame({'Percentage': [44, 17, 12, 5, 4]}, index=['Organics', 'Paper', 'Plastic', 'Glass', 'Metal']))

with col_cam:
    st.write("### 📸 AI Vision Analysis")
    st.camera_input("Capture Waste Pile", key="cam")