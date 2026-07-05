import streamlit as st
from google.cloud import bigquery
import pandas as pd
import vertexai
from vertexai.generative_models import GenerativeModel

# Set up page config
st.set_page_config(page_title="Future Forge Eco Platform", page_icon="🌍", layout="wide")

st.title("🌍 Future Forge: Waste Management & Resource Optimization")
st.markdown("Automated sustainability metrics and AI-powered efficiency recommendations.")

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
        SELECT log_date, facility_location, material_type, 
               generated_waste_kg, recycled_waste_kg, 
               energy_consumption_kwh, resource_efficiency_score 
        FROM `{project_id}.eco_efficiency.waste_resource_logs`
        ORDER BY log_date DESC
    """
    return client.query(query).to_dataframe()

try:
    df = load_data()
    
    # --- DYNAMIC SEARCH BAR ---
    st.markdown("---")
    search_query = st.text_input(
        "🔍 Search Operations:", 
        placeholder="Type a facility name or material type (e.g., 'Data Center', 'Plastic', 'Hub B')..."
    )
    
    # Filter dataset dynamically based on search query
    if search_query:
        df_filtered = df[
            df['facility_location'].str.contains(search_query, case=False, na=False) | 
            df['material_type'].str.contains(search_query, case=False, na=False)
        ]
        st.caption(f"Showing {len(df_filtered)} of {len(df)} operational records matching '{search_query}'")
    else:
        df_filtered = df

    # --- METRIC CARDS (Using Filtered Data) ---
    col1, col2, col3 = st.columns(3)
    with col1:
        total_waste = df_filtered['generated_waste_kg'].sum()
        st.metric(label="Total Generated Waste", value=f"{total_waste:,.1f} kg")
    with col2:
        total_recycled = df_filtered['recycled_waste_kg'].sum()
        rate = (total_recycled / total_waste * 100) if total_waste > 0 else 0
        st.metric(label="Total Recycled Material", value=f"{total_recycled:,.1f} kg", delta=f"{rate:.1f}% Rate")
    with col3:
        avg_efficiency = df_filtered['resource_efficiency_score'].mean() if not df_filtered.empty else 0
        st.metric(label="Avg Efficiency Score", value=f"{avg_efficiency:.1f} / 100")

    # --- VISUAL ANALYTICS ---
    st.subheader("📊 Waste Analytics Breakdown")
    if not df_filtered.empty:
        chart_data = df_filtered.groupby('facility_location')[['generated_waste_kg', 'recycled_waste_kg']].sum()
        st.bar_chart(chart_data)
    else:
        st.warning("No data available for the current search criteria to chart.")

    # --- DATA TABLE ---
    st.subheader("📋 Operational Efficiency Logs")
    st.dataframe(df_filtered, use_container_width=True)

    # --- AI INSIGHTS ---
    st.markdown("---")
    st.subheader("🤖 Gemini Resource Optimization Engine")
    
    if st.button("Generate Live AI Sustainability Strategy"):
        if df_filtered.empty:
            st.error("Cannot generate strategy. The filtered dataset is completely empty.")
        else:
            with st.spinner("Gemini is evaluating your scoped data warehouse logs..."):
                try:
                    data_summary = df_filtered.to_string(index=False)
                    
                    prompt = f"""
                    You are the core AI engine for the Future Forge Eco Platform. 
                    Analyze these specific filtered facility resource logs for operational inefficiencies and provide explicit, highly actionable executive recommendations to minimize material waste, boost recycling rates, and optimize energy overhead:

                    {data_summary}
                    """
                    
                    response = ai_model.generate_content(prompt)
                    st.success("🌍 Live Target AI Analysis Complete!")
                    st.markdown(response.text)
                    
                except Exception as ai_err:
                    st.error(f"Could not connect to Gemini Engine: {ai_err}")

except Exception as e:
    st.error(f"Could not connect to BigQuery: {e}")
