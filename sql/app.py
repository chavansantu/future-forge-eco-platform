import streamlit as st
import pandas as pd
from google.cloud import bigquery
import vertexai
from vertexai.generative_models import GenerativeModel

# =====================================================================
# 1. Streamlit Application Page Configuration & Styling
# =====================================================================
st.set_page_config(
    page_title="Future Forge Eco-Platform",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🌱 Future Forge Eco-Platform: Generative AI Public Health Insights")
st.markdown("---")

# =====================================================================
# 2. BigQuery Data Ingestion Layer
# =====================================================================
@st.cache_data(ttl=600)  # Cache metrics for 10 minutes to manage query costs
def load_pipeline_data():
    # Cloud Shell automatically attaches your current login credentials
    client = bigquery.Client()
    
    query = """
        SELECT 
          city,
          avg_pm25,
          cases,
          priority_score,
          ai_reasoning
        FROM `future-forge-eco-platform.community_wellness.vw_actionable_insights_ai`
        ORDER BY priority_score DESC;
    """
    query_job = client.query(query)
    return query_job.to_dataframe()

# Attempt connection to the BigQuery warehouse view
try:
    df = load_pipeline_data()
except Exception as e:
    st.error(f"Error connecting to Google Cloud BigQuery: {e}")
    df = pd.DataFrame()  # Fallback empty dataframe to prevent application crash

# =====================================================================
# 3. Core Dashboard Layout & Interactive Command Panel
# =====================================================================
if not df.empty:
    st.subheader("📊 Operational City Command Center")
    
    # Render regional picker dropdown in the sidebar panel
    cities = df['city'].unique()
    selected_city = st.sidebar.selectbox("🎯 Target Monitoring Zone", cities)
    
    # Isolate records for the specific selected municipality
    city_data = df[df['city'] == selected_city].iloc[0]
    
    # Layout 3 operational data metrics columns
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Average PM2.5 Level", value=f"{city_data['avg_pm25']} µg/m³")
    with col2:
        st.metric(label="Clinical Respiratory Admissions", value=f"{city_data['cases']} Cases")
    with col3:
        score = city_data['priority_score']
        st.metric(label="Hazard Priority Risk Score", value=f"{score:.2f}")

    st.markdown("---")

    # =====================================================================
    # 4. Warehouse Resident AI Generation Insights
    # =====================================================================
    st.subheader(f"🤖 Automated Gemini Action Plan: {selected_city}")
    
    with st.container():
        st.info("The text below is pulled directly from pre-computed BQML text generation workloads running over cloud-hosted NVIDIA Tensor Core GPUs.")
        st.markdown(f"**Intervention Directive:**\n\n{city_data['ai_reasoning']}")

    st.markdown("---")

    # =====================================================================
    # 5. Live Interactive Copilot Core Agent (Deep-Dive Add-on Feature)
    # =====================================================================
    st.subheader("💬 Deep-Dive Interactive AI Agent")
    st.write("Need real-time asset logistics coordination? Input custom follow-up inquiries directly to the active cluster model:")
    
    user_query = st.text_input(
        label="Enter command prompt", 
        placeholder=f"e.g., Draft a brief municipal health alert broadcast text regarding conditions in {selected_city}...",
        label_visibility="collapsed"
    )
    
    if user_query:
        with st.spinner("AI Agent synthesizing structural deployment strategies over Vertex AI acceleration..."):
            try:
                # Initialize Vertex AI framework using current Cloud Shell sandbox variables
                # The SDK will auto-detect the project boundary
                client_bq = bigquery.Client()
                project_id = client_bq.project
                
                vertexai.init(project=project_id, location="us-central1")
                
                # Bundle background data rows right into the execution prompt for deep context
                contextual_prompt = f"""
                You are the Future Forge Eco-Platform AI Agent.
                Operational metrics for context regarding {selected_city}:
                - Core PM2.5 Level: {city_data['avg_pm25']} µg/m³
                - Local Hospital Respiratory Cases: {city_data['cases']}
                - Calculated Hazard Priority Risk: {city_data['priority_score']}
                
                User Request: {user_query}
                Provide an expert, rapid, completely structured crisis coordination response.
                """
                
                # Spin up an instantaneous auxiliary context run via Gemini 1.5 Flash
                model = GenerativeModel("gemini-1.5-flash")
                response = model.generate_content(contextual_prompt)
                
                st.markdown(f"### 📋 Custom Tactical Response:\n{response.text}")
                
            except Exception as e:
                st.warning(f"Vertex AI Interactive Agent initialization exception: {e}")
                st.info("💡 Ensure the Vertex AI User IAM permission is activated for your execution profile to unlock full conversational mode.")

else:
    st.warning("Establishing secure interface connection pipelines. Verify your underlying BigQuery dataset and dataset location settings...")