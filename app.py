import streamlit as st
from google.cloud import bigquery
import pandas as pd
import vertexai
from vertexai.generative_models import GenerativeModel

# Set up page config
st.set_page_config(page_title="Future Forge Global Eco Platform", page_icon="🌍", layout="wide")

st.title("🌍 Future Forge: Global Waste Management & Resource Optimization")
st.markdown("Macro-economic sustainability monitoring and sovereign AI-powered mitigation strategies.")

# Initialize Project Details
project_id = "future-forge-eco-platform"
client = bigquery.Client(project=project_id)

# Initialize Vertex AI Core
vertexai.init(project=project_id, location="us-central1")
ai_model = GenerativeModel("gemini-1.5-flash")

# Fetch Data from BigQuery
@st.cache_data
def load_data():
    query = f"""
        SELECT log_date, country, facility_location, material_type, 
               generated_waste_kg, recycled_waste_kg, 
               energy_consumption_kwh, resource_efficiency_score 
        FROM `{project_id}.eco_efficiency.waste_resource_logs`
        ORDER BY generated_waste_kg DESC
    """
    return client.query(query).to_dataframe()

try:
    df = load_data()
    
    # --- SIDEBAR INTERACTIVE FILTERS ---
    st.sidebar.header("🗺️ Geographic Navigation")
    unique_countries = ["All Global Regions"] + list(df['country'].unique())
    selected_country = st.sidebar.selectbox("Select Target Country/Region:", unique_countries)
    
    # Text Search Layer
    search_query = st.sidebar.text_input("🔍 Keyword Filter:", placeholder="e.g. E-waste, Munich...")

    # Apply Filters Dynamically
    df_filtered = df.copy()
    if selected_country != "All Global Regions":
        df_filtered = df_filtered[df_filtered['country'] == selected_country]
        
    if search_query:
        df_filtered = df_filtered[
            df_filtered['facility_location'].str.contains(search_query, case=False, na=False) | 
            df_filtered['material_type'].str.contains(search_query, case=False, na=False)
        ]

    # --- METRIC CARDS ---
    col1, col2, col3 = st.columns(3)
    with col1:
        total_waste = df_filtered['generated_waste_kg'].sum()
        st.metric(label=f"Total Waste ({selected_country})", value=f"{total_waste:,.1f} kg")
    with col2:
        total_recycled = df_filtered['recycled_waste_kg'].sum()
        rate = (total_recycled / total_waste * 100) if total_waste > 0 else 0
        st.metric(label="Regional Recycling Efficiency", value=f"{total_recycled:,.1f} kg", delta=f"{rate:.1f}% Recovery")
    with col3:
        avg_efficiency = df_filtered['resource_efficiency_score'].mean() if not df_filtered.empty else 0
        st.metric(label="Mean Sustainability Score", value=f"{avg_efficiency:.1f} / 100")

    # --- VISUAL ANALYTICS ---
    st.subheader("📊 Cross-Border Environmental Metrics")
    if not df_filtered.empty:
        # Toggle chart layout based on context
        group_col = 'facility_location' if selected_country != "All Global Regions" else 'country'
        chart_data = df_filtered.groupby(group_col)[['generated_waste_kg', 'recycled_waste_kg']].sum()
        st.bar_chart(chart_data)
    else:
        st.warning("No operational data records fit your applied filters.")

    # --- DATA GRID ---
    st.subheader(f"📋 Live Ledger: {selected_country} Logs")
    st.dataframe(df_filtered, use_container_width=True)

    # --- AI STRATEGY ENGINE ---
    st.markdown("---")
    st.subheader(f"🤖 Gemini Regional Policy Advisor ({selected_country})")
    
    if st.button("Generate Live Sovereign AI Strategy"):
        if df_filtered.empty:
            st.error("The filtered metric profile is empty. Cannot extract insights.")
        else:
            with st.spinner(f"Gemini is analyzing industrial records for {selected_country}..."):
                try:
                    data_summary = df_filtered.to_string(index=False)
                    
                    prompt = f"""
                    You are the Head Global AI Environmental Strategist for the Future Forge Platform. 
                    Analyze these specific industrial telemetry logs for the selected geography context: '{selected_country}'. 
                    
                    Provide 3 rigorous, hyper-localized economic and operational recommendations to minimize industrial output waste, maximize macro recycling infrastructure, and curb heavy energy dependencies based entirely on this data footprint:

                    {data_summary}
                    """
                    
                    response = ai_model.generate_content(prompt)
                    st.success(f"🌍 Strategy Briefing Formulated for {selected_country}!")
                    st.markdown(response.text)
                    
                except Exception as ai_err:
                    st.error(f"Vertex AI Connection Failed: {ai_err}")

except Exception as e:
    st.error(f"Data Connection Failure: {e}")
