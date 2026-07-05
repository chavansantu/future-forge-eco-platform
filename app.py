import streamlit as st
from google.cloud import bigquery
import pandas as pd

# Set up page config
st.set_page_config(page_title="Future Forge Eco Platform", page_icon="🌍", layout="wide")

st.title("🌍 Future Forge: Waste Management & Resource Optimization")
st.markdown("Automated sustainability metrics and AI-powered efficiency recommendations.")

# Initialize BigQuery Client
project_id = "future-forge-eco-platform"
client = bigquery.Client(project=project_id)

# Fetch Data from our new table
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

    # --- DATA TABLE ---
    st.subheader("📋 Operational Efficiency Logs")
    st.dataframe(df, use_container_width=True)

    # --- AI INSIGHTS ---
    st.markdown("---")
    st.subheader("🤖 Gemini Resource Optimization Engine")
    
    if st.button("Generate AI Sustainability Strategy"):
        with st.spinner("Gemini is evaluating your operational logs..."):
            # Format data brief for the prompt
            data_summary = df.to_string(index=False)
            
            # Using BigQuery ML remote model structure to call Gemini directly via SQL
            ai_query = f"""
                SELECT response
                FROM ML.GENERATE_TEXT(
                    MODEL `{project_id}.eco_efficiency.gemini_model`,
                    (SELECT 'Analyze this facility data for inefficiencies and provide 3 explicit, actionable recommendations to reduce material waste and optimize energy use:\n\n{data_summary}' AS prompt),
                    STRUCT(0.2 AS temperature, 1024 AS max_output_tokens)
                )
            """
            try:
                ai_result = client.query(ai_query).to_dataframe()
                st.success("Analysis Complete!")
                st.write(ai_result['response'].values[0])
            except Exception as e:
                st.info("💡 Database model connection pending. Here is an immediate structural mock up:")
                st.write("1. **Optimize Cooling at Data Center A:** Your current energy consumption relative to e-waste is high. Shifting computing workloads to off-peak hours could reduce overhead.")
                st.write("2. **Upcycle Plastic Packaging at Logistics Hub B:** Plastic volume is high. Introduce a localized closed-loop shredding pipeline.")

except Exception as e:
    st.error(f"Could not connect to BigQuery: {e}")
    st.info("Ensure you have run the data injection SQL script and your dataset is named 'eco_efficiency'.")
