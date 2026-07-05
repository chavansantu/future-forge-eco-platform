from google.cloud import bigquery

project_id = "future-forge-eco-platform"
client = bigquery.Client(project=project_id)

sql = """
CREATE OR REPLACE TABLE `future-forge-eco-platform.eco_efficiency.waste_resource_logs` (
    log_date DATE,
    country STRING,
    facility_location STRING,
    material_type STRING,        
    generated_waste_kg NUMERIC,
    recycled_waste_kg NUMERIC,
    energy_consumption_kwh NUMERIC,
    resource_efficiency_score NUMERIC
);

INSERT INTO `future-forge-eco-platform.eco_efficiency.waste_resource_logs` (log_date, country, facility_location, material_type, generated_waste_kg, recycled_waste_kg, energy_consumption_kwh, resource_efficiency_score)
VALUES 
    ('2026-07-01', 'India', 'Bengaluru Tech Park', 'E-waste', 1450.2, 1280.0, 14200.5, 88.2),
    ('2026-07-02', 'India', 'Mumbai Logistics Hub', 'Plastic Packaging', 3200.5, 2150.2, 9800.0, 67.1),
    ('2026-07-05', 'India', 'Delhi Manufacturing Unit', 'Industrial Scrap', 5400.0, 4100.0, 31000.0, 75.4),
    ('2026-07-02', 'China', 'Shenzhen Manufacturing Plant', 'Industrial Scrap', 8950.0, 7100.5, 45300.2, 79.3),
    ('2026-07-03', 'China', 'Shanghai Distribution Center', 'Plastic Packaging', 4120.0, 3900.0, 11200.7, 94.6),
    ('2026-07-06', 'China', 'Beijing Electronics Hub', 'E-waste', 2300.0, 2150.0, 18500.0, 93.5),
    ('2026-07-03', 'Russia', 'Siberian Industrial Complex', 'Heavy Metals & Scrap', 12450.0, 6200.0, 89100.4, 49.8),
    ('2026-07-04', 'Russia', 'Moscow Data Center', 'E-waste', 850.0, 810.0, 24500.6, 95.2),
    ('2026-07-04', 'United States', 'Silicon Valley Cluster', 'E-waste', 2100.4, 1950.0, 53000.2, 92.8),
    ('2026-07-06', 'United States', 'Texas Distribution Hub', 'Plastic Packaging', 6100.2, 4200.5, 14200.0, 68.9),
    ('2026-07-05', 'Germany', 'Munich Logistics Center', 'Paper & Organic', 1100.0, 1050.0, 4300.1, 95.4),
    ('2026-07-07', 'Germany', 'Stuttgart Automotive Plant', 'Industrial Scrap', 9800.0, 8200.0, 64000.0, 83.7),
    ('2026-07-06', 'Japan', 'Tokyo Robotics Lab', 'E-waste', 1200.5, 1150.0, 22000.3, 95.8),
    ('2026-07-07', 'Japan', 'Osaka Supply Node', 'Plastic Packaging', 3400.0, 3100.0, 8900.0, 91.2),
    ('2026-07-05', 'Brazil', 'São Paulo Sorting Facility', 'Paper & Organic', 4500.2, 3800.0, 7200.4, 84.4),
    ('2026-07-07', 'South Africa', 'Johannesburg Hub', 'Industrial Scrap', 7200.0, 4900.0, 29000.0, 68.1);
"""

print("Injecting expanded global environment rows into BigQuery...")
query_job = client.query(sql)
query_job.result()
print("🎉 Success! Comprehensive global dataset is live.")
