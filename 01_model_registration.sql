-- Step 1: Registering Gemini 2.5 Flash inside BigQuery ML
CREATE OR REPLACE MODEL `future-forge-eco-platform.community_wellness.gemini_flash_model`
REMOTE WITH CONNECTION `future-forge-eco-platform.us.vertex_ai_connection`
OPTIONS(ENDPOINT = 'gemini-2.5-flash');