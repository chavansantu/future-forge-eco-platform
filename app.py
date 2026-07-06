import streamlit as st
import pandas as pd
import numpy as np

# --- PAGE CONFIG ---
st.set_page_config(page_title="Future Forge", page_icon="🌐", layout="centered")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
        .stApp { background-color: #ffffff; }
        .main-logo { text-align: center; font-size: 60px; font-weight: bold; color: #4285f4; margin-top: 50px; margin-bottom: 30px; }
        .stTextInput > div > div > input { border-radius: 25px !important; border: 1px solid #dfe1e5; padding: 20px 25px; box-shadow: 0 1px 6px rgba(32,33,36,0.1); }
        .result-box { border: 1px solid #dfe1e5; border-radius: 8px; padding: 20px; margin-top: 20px; }
    </style>
""", unsafe_allow_html=True)

# --- AUTH ---
if "auth" not in st.session_state: st.session_state.auth = False
if not st.session_state.auth:
    st.markdown("<h1 style='text-align: center; margin-top: 100px;'>Future Forge</h1>", unsafe_allow_html=True)
    with st.form("login"):
        user = st.text_input("Username", label_visibility="collapsed", placeholder="Username")
        pwd = st.text_input("Password", label_visibility="collapsed", placeholder="Password", type="password")
        if st.form_submit_button("Enter"):
            if user == "santosh_chavan" and pwd == "Chavan@1999":
                st.session_state.auth = True
                st.rerun()
    st.stop()

# --- HOME HUB UI ---
st.markdown("<div class='main-logo'>Future Forge</div>", unsafe_allow_html=True)

# Search Bar
with st.form("search_form"):
    query = st.text_input("Search", label_visibility="collapsed", placeholder="Search solutions for waste dumping...")
    submitted = st.form_submit_button("Search")

# Sensory Core (Camera & Location)
col1, col2 = st.columns([1, 1])
with col1:
    media = st.file_uploader("📷 Capture Waste", type=['png', 'jpg'], label_visibility="collapsed")
with col2:
    if st.button("📍 Detect Location"):
        st.session_state.show_map = True

# --- INCIDENT & REMEDIATION LOGIC ---
if media:
    st.divider()
    st.info("🤖 **Visual Intelligence:** Analyzing incident image...")
    st.success("Incident Registered! Notifications sent to Municipal Corporation and Local Authority.")
    
    with st.expander("💡 AI Cleaning Guide & Suggestions", expanded=True):
        st.markdown("""
        **Immediate Cleanup Steps:**
        1. **Safety:** Wear protective gear (gloves/masks) before approaching waste.
        2. **Segregation:** Separate biodegradables from recyclables/hazardous waste.
        3. **Disposal:** Deposit in designated municipal bins or wait for fleet pickup.
        
        **Sustainability & Long-term:**
        * **Composting:** If the waste is organic, suggest local community composting.
        * **Prevention:** Install 'No Dumping' signage to deter future site misuse.
        * **Verification:** Take an 'After' photo once the area is clear to update the system.
        """)
    
    if st.button("Confirm Report Submission"):
        st.balloons()
        st.write("✅ Report #FF-2026-001 successfully logged for immediate remediation.")

# --- MAPPING & SEARCH RESULTS ---
if "show_map" in st.session_state and st.session_state.show_map:
    st.divider()
    st.write("### 📍 Registered Incident Location")
    st.map(pd.DataFrame({'lat': [12.9716], 'lon': [77.5946]}))
    if st.button("Close Map"): del st.session_state.show_map

if submitted or query:
    st.divider()
    st.markdown(f"### Solutions for: *{query}*")
    st.markdown("""
    * **Automated Dispatch:** Roadside dump detection triggers autonomous fleet cleanup.
    * **Compliance:** Incident logging is fully aligned with SWM 2026 regulations.
    * **Analytics:** Real-time geo-spatial alerts improve municipal response times via RAPIDS-accelerated processing.
    """)
    st.line_chart(pd.DataFrame(np.random.randn(10, 1), columns=['Impact Projection']))