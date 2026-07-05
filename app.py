import streamlit as st
from google.cloud import bigquery
import pandas as pd
import vertexai
from vertexai.generative_models import GenerativeModel

# Set up page config
st.set_page_config(page_title="Future Forge Global Search Engine", page_icon="🌍", layout="wide")

st.title("🌍 Future Forge: Global Sustainability Intel & Engine")
st.markdown("Query country profiles, factory hubs, and material volumes via unified AI search tracking.")

# Initialize Project Details
project_id = "future-forge-eco-platform"
client = bigquery.Client(project=project_id)

# Initialize Vertex AI Core
vertexai.init(project=project_id, location="us-central1")
ai_model = GenerativeModel("gemini-1.5-flash")

# Fetch Data Live
def load_data():
    query = f"""
        SELECT log_date, country, facility_location, material_type, 
               generated_waste_kg, recycled_waste_kg, 
               energy_consumption_kwh, resource_efficiency_score 
        FROM `{project_id}.eco_efficiency.waste_resource_logs`
        ORDER BY log_date DESC
    """
    return client.query(query).to_dataframe()

try:
    df = load_data()
    
    # --- GLOBAL TEXT FILTER SEARCH ENGINE ---
    st.subheader("🔍 Enterprise Environmental Search Engine")
    search_query = st.text_input(
        "Search cross-border metrics or ask a question:", 
        placeholder="Type a keyword (e.g. 'India') or ask a question (e.g. 'which city in India produces more waste?')..."
    )

    # Initialize data views
    df_filtered = df.copy()
    ai_natural_language_response = None

    if search_query:
        # 1. Try traditional keyword filter first
        keyword_matches = df[
            df['country'].str.contains(search_query, case=False, na=False) | 
            df['facility_location'].str.contains(search_query, case=False, na=False) | 
            df['material_type'].str.contains(search_query, case=False, na=False)
        ]
        
        # 2. If no direct keyword match, it's a natural language question! Activate Gemini.
        if keyword_matches.empty:
            st.info("🤖 No direct keyword matches found. Activating Gemini Semantic Intelligence to interpret your question...")
            with st.spinner("Gemini is reading the global data ledger to answer your question..."):
                try:
                    data_context = df.to_string(index=False)
                    prompt = f"""
                    You are the Intelligent Search Interface for the Future Forge Platform.
                    The user asked this natural language question: "{search_query}"
                    
                    Here is the complete live data ledger from the database:
                    {data_context}
                    
                    Task:
                    1. Answer their question directly and concisely based on the data provided (e.g., explicitly calculate sums or compare cities if requested).
                    2. Identify if they are talking about a specific country or material in our dataset. At the very end of your response, output a single line format like this: FILTER_HINT: [Country Name or Material Type] so we can filter the visual map for them.
                    """
                    response = ai_model.generate_content(prompt)
                    ai_natural_language_response = response.text
                    
                    # Check if Gemini gave us a filter hint to isolate rows
                    if "FILTER_HINT:" in ai_natural_language_response:
                        parts = ai_natural_language_response.split("FILTER_HINT:")
                        hint = parts[1].strip().strip("[]\"'")
                        ai_natural_language_response = parts[0] # Clean the visible text
                        
                        # Apply dynamic filter based on AI extraction
                        df_filtered = df[
                            df['country'].str.contains(hint, case=False, na=False) |
                            df['facility_location'].str.contains(hint, case=False, na=False) |
                            df['material_type'].str.contains(hint, case=False, na=False)
                        ]
                except Exception as ai_err:
                    st.error(f"AI Search Engine parser offline: {ai_err}")
        else:
            df_filtered = keyword_matches
            st.success(f"🔍 Direct database index match: Found {len(df_filtered)} records.")

    # --- DISPLAY AI ANSWER IF AVAILABLE ---
    if ai_natural_language_response:
        st.chat_message("assistant").markdown(ai_natural_language_response)

    # --- METRIC CARDS ---
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        total_waste = df_filtered['generated_waste_kg'].sum()
        st.metric(label="Selected Gross Waste", value=f"{total_waste:,.1f} kg")
    with col2:
        total_recycled = df_filtered['recycled_waste_kg'].sum()
        rate = (total_recycled / total_waste * 100) if total_waste > 0 else 0
        st.metric(label="Selected Diversion Rate", value=f"{total_recycled:,.1f} kg", delta=f"{rate:.1f}% Recycled")
    with col3:
        avg_efficiency = df_filtered['resource_efficiency_score'].mean() if not df_filtered.empty else 0
        st.metric(label="Selected Efficiency Target", value=f"{avg_efficiency:.1f} / 100")

    # --- VISUAL GRAPH ENGINE ---
    st.subheader("📊 Cross-Border Environmental Metrics Breakdown")
    if not df_filtered.empty:
        chart_group = 'facility_location' if len(df_filtered['country'].unique()) == 1 else 'country'
        chart_data = df_filtered.groupby(chart_group)[['generated_waste_kg', 'recycled_waste_kg']].sum()
        st.bar_chart(chart_data)
    else:
        st.warning("No operational data records match this scope.")

    # --- DATA GRID ---
    st.subheader("📋 Filtered Operational Live Ledger")
    display_df = df_filtered.copy()
    display_df.columns = [
        "Log Date", "Country", "Facility Location", "Material Type", 
        "Generated Waste (kg)", "Recycled Waste (kg)", "Energy Consumption (kWh)", "Resource Efficiency Score"
    ]
    st.dataframe(display_df, use_container_width=True)

    # --- BOTTOM AI STRATEGY ENGINE ---
    st.markdown("---")
    st.subheader("🤖 Comprehensive Deep-Dive Optimization Strategy")
    if st.button("Generate Tactical Action Plan"):
        with st.spinner("Analyzing operational vectors..."):
            try:
                data_summary = df_filtered.to_string(index=False)
                prompt = f"""
                Provide an executive 3-point strategy for these specific records:
                {data_summary}
                """
                response = ai_model.generate_content(prompt)
                st.markdown(response.text)
            except Exception as e:
                st.error(f"Strategy engine failed: {e}")

except Exception as e:
    st.error(f"Database Read Blocked: {e}")
