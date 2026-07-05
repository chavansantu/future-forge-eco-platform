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
    ('2026-07-02', 'China', 'Shenzhen Manufacturing Plant', 'Industrial Scrap', 8950.0, 7100.5, 45300.2, 79.3),
    ('2026-07-03', 'China', 'Shanghai Distribution Center', 'Plastic Packaging', 4120.0, 3900.0, 11200.7, 94.6),
    ('2026-07-03', 'Russia', 'Siberian Industrial Complex', 'Heavy Metals & Scrap', 12450.0, 6200.0, 89100.4, 49.8),
    ('2026-07-04', 'Russia', 'Moscow Data Center', 'E-waste', 850.0, 810.0, 24500.6, 95.2),
    ('2026-07-04', 'United States', 'Silicon Valley Cluster', 'E-waste', 2100.4, 1950.0, 53000.2, 92.8),
    ('2026-07-05', 'Germany', 'Munich Logistics Center', 'Paper & Organic', 1100.0, 1050.0, 4300.1, 95.4);
