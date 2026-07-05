import streamlit as st
import pandas as pd
from google.cloud import bigquery
import vertexai
from vertexai.generative_models import GenerativeModel

st.set_page_config(page_title="Future Forge Eco-Platform", page_icon="🌱", layout="wide")
st.title("🌱 Future Forge Eco-Platform: Generative AI Public Health Insights")
st.markdown("---")

@st.cache_data(ttl=600)
def load_pipeline_data():
    client = bigquery.Client()
    query = """
        SELECT city, avg_pm25, cases, priority_score, ai_reasoning
        FROM `future-forge-eco-platform.community_wellness.vw_actionable_insights_ai`
        ORDER BY priority_score DESC;
    """
    return client.query(query).to_dataframe()

try:
    df = load_pipeline_data()
except Exception as e:
    st.error(f"Error connecting to Google Cloud BigQuery: {e}")
    df = pd.DataFrame()

if not df.empty:
    st.subheader("📊 Operational City Command Center")
    selected_city = st.sidebar.selectbox("🎯 Target Monitoring Zone", df['city'].unique())
    city_data = df[df['city'] == selected_city].iloc[0]
    
    col1, col2, col3 = st.columns(3)
    with col1: st.metric(label="Average PM2.5 Level", value=f"{city_data['avg_pm25']} µg/m³")
    with col2: st.metric(label="Clinical Respiratory Admissions", value=f"{city_data['cases']} Cases")
    with col3: st.metric(label="Hazard Priority Risk Score", value=f"{city_data['priority_score']:.2f}")

    st.markdown("---")
    st.subheader(f"🤖 Automated Gemini Action Plan: {selected_city}")
    st.info("Pulled directly from pre-computed BQML workloads over NVIDIA Tensor Core GPUs.")
    st.markdown(f"**Intervention Directive:**\n\n{city_data['ai_reasoning']}")

    st.markdown("---")
    st.subheader("💬 Deep-Dive Interactive AI Agent")
    user_query = st.text_input(label="Enter command prompt", placeholder="Ask a tactical follow-up question...", label_visibility="collapsed")
    
    if user_query:
        with st.spinner("AI Agent synthesizing deployment strategies..."):
            try:
                client_bq = bigquery.Client()
                vertexai.init(project=client_bq.project, location="us-central1")
                context = f"City: {selected_city}, PM2.5: {city_data['avg_pm25']}, Cases: {city_data['cases']}. Request: {user_query}"
                model = GenerativeModel("gemini-2.5-flash")
                st.markdown(f"### 📋 Response:\n{model.generate_content(context).text}")
            except Exception as e:
                st.warning(f"Vertex AI initialization exception: {e}")
else:
    st.warning("Awaiting secure streaming connection from the BigQuery data warehouse layer...")
