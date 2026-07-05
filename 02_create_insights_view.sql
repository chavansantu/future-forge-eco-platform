-- Step 2: Creating the live semantic view to feed Looker Studio
CREATE OR REPLACE VIEW `future-forge-eco-platform.community_wellness.vw_actionable_insights_ai` AS
SELECT 
  city,
  avg_pm25,
  cases,
  priority_score,
  ml_generate_text_llm_result AS ai_reasoning
FROM 
  ML.GENERATE_TEXT(
    MODEL `future-forge-eco-platform.community_wellness.gemini_flash_model`,
    (
      SELECT 
        city,
        avg_pm25,
        cases,
        priority_score,
        CONCAT(
          'Analyze the public health hazard status for ', city, 
          '. The average PM2.5 level is ', CAST(avg_pm25 AS STRING), 
          ' micrograms per cubic meter and clinical respiratory admissions are at ', CAST(cases AS STRING), 
          ' cases. Provide a highly actionable, scannable public health intervention summary.'
        ) AS prompt
      FROM `future-forge-eco-platform.community_wellness.actionable_insights`
    ),
    STRUCT(
      0.2 AS temperature, 
      1024 AS max_output_tokens,
      TRUE AS flatten_json_output
    )
  );