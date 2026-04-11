# Flood Risk Predictor - Model V3 Upgrade Report

This document outlines the major technical and visual upgrades performed during the transition to **Model V3 (High-Performance XGBoost)**.

## 🚀 Key Improvements

### 1. High-Precision XGBoost Model
- **New Feature Schema**: Upgraded from 49 to **52 engineered features**.
- **Performance Metrics**:
    - **AUC**: 0.9623
    - **F1-Score**: 0.5032
    - **MCC**: 0.4960
- **Model Type**: Refreshed XGBoost architecture trained on an expanded All-India dataset (2023-2024).

### 2. Live Satellite Data Integration (NASA POWER API)
- **Real SMAP Data**: The system now connects directly to the **NASA POWER API** (`power.larc.nasa.gov`) to fetch live satellite soil moisture data (**GWETROOT**).
- **Physics-Based Fallback**: Maintained a robust fallback system that uses physics-based proxies if the NASA API is unreachable, ensuring zero downtime.
- **Improved SMAP Features**:
    - `SMAP_7Day_Avg`: Mean soil wetness over the last week.
    - `SMAP_3Day_Max`: Peak soil wetness over the last 3 days.
    - `Rain_on_Wet_Soil`: Interaction feature calculating rainfall impact on saturated ground.

### 3. 4-Tier Risk Classification System
The prediction logic has been refined into a standard 4-tier system for better granularity:
- **Low Risk**: < 20% probability
- **Moderate Risk**: 20% – 40% probability
- **High Risk**: 40% – 65% probability
- **Very High Risk**: ≥ 65% probability

### 4. Professional UI Overhaul
- **Model Performance Panel**: Added a new collapsible dashboard component showing live model metrics (AUC, F1, Accuracy).
- **Clean Aesthetic**: Removed emoji icons (📊, ✓, etc.) in favor of a sleek, professional "Enterprise-grade" design.
- **Dynamic Alerts**: Updated `AlertNotification` and `FloodRiskIndicator` to highlight the new "Very High" risk tier with unique styling and urgent messaging.
- **Footer Updates**: Updated labels to correctly reflect **Model V3 (52 features)** and **NASA API** data sourcing.

## 🛠 Technical Stack Changes
- **Backend**: Updated `model_loader.py`, `app.py`, and `weather_fetcher.py` to handle the new 52-column feature vectors and API fetching.
- **Frontend**: Modified React components (`Dashboard`, `AlertNotification`, `FloodRiskIndicator`) to support the 4-tier risk data structure.
- **Deployment**: Configured internal path logic to support direct manual uploads to Hugging Face Spaces (handling the `model/new_model/` directory structure).

---
*Generated on: 2026-04-11*
