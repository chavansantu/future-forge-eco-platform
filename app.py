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
    
    # --- METRIC CARDS ---
    col1, col2, col3 = st.columns(3)
    with col1:
        total_waste = df['generated_waste_kg'].sum()
        st.metric(label="Total Generated Waste", value=f"{total_waste:,.1f} kg")
    with col2:
        total_recycled = df['recycled_waste_kg'].sum()
        st.metric(label="Total Recycled Material", value=f"{total_recycled:,.1f} kg", delta=f"{(total_recycled/total_waste)*100:.1f}% Rate")
    with col3:
        avg_efficiency = df['resource_efficiency_score'].mean()
        st.metric(label="Avg Efficiency Score", value=f"{avg_efficiency:.1f} / 100")

    # --- VISUAL ANALYTICS ---
    st.subheader("📊 Waste Analytics Breakdown by Facility")
    
    # Restructure data for a clean side-by-side comparison chart
    chart_data = df.groupby('facility_location')[['generated_waste_kg', 'recycled_waste_kg']].sum()
    st.bar_chart(chart_data)

    # --- DATA TABLE ---
    st.subheader("📋 Operational Efficiency Logs")
    st.dataframe(df, use_container_width=True)

    # --- AI INSIGHTS ---
    st.markdown("---")
    st.subheader("🤖 Gemini Resource Optimization Engine")
    
    if st.button("Generate Live AI Sustainability Strategy"):
        with st.spinner("Gemini is evaluating your live data warehouse logs..."):
            try:
                data_summary = df.to_string(index=False)
                
                prompt = f"""
                You are the core AI core engine for the Future Forge Eco Platform. 
                Analyze these facility resource logs for operational inefficiencies and provide 3 explicit, highly actionable executive recommendations to minimize material waste, boost recycling rates, and optimize energy overhead:

                {data_summary}
                """
                
                response = ai_model.generate_content(prompt)
                st.success("🌍 Live AI Analysis Complete!")
                st.markdown(response.text)
                
            except Exception as ai_err:
                st.error(f"Could not connect to Gemini Engine: {ai_err}")

except Exception as e:
    st.error(f"Could not connect to BigQuery: {e}")
