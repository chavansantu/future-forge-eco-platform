# Future Forge Eco-Platform: Generative AI Public Health Insights

An enterprise-grade reference architecture pairing Google Cloud data warehouse infrastructure with accelerated backend generative AI processing to generate real-time public health interventions.

## 🏗️ Reference Architecture
* **Google Cloud Data Layer:** High-throughput clinical respiratory admission records and spatial environmental metrics (`avg_pm25`) are securely managed within **Google BigQuery**.
* **NVIDIA Acceleration Layer:** Built using native **BigQuery ML (BQML)** to completely eliminate intermediate application data egress. Inference tasks are processed in a parallel layout over cloud-hosted **NVIDIA Tensor Core GPUs** using the **Gemini Enterprise Agent Platform (Gemini 2.5 Flash)**.
* **Application + Decision Layer:** Exposed via a dynamic database view directly to an operational **Looker Studio** command dashboard for real-time regional triage.

## 📊 User-Visible Decision Improvement
* **Before:** Healthcare workers had to manually download and cross-reference messy environmental spreadsheets with emergency hospital metrics—introducing high latency and data silos.
* **After:** Public health directors use an interactive visual dashboard that surfaces an explicit target priority risk score and an instantly actionable, wrapped plain-language text intervention summary.

## 🖥️ Live System Preview
![Looker Studio Dashboard Workspace](./assets/dashboard_preview.jpeg)