# Flood Risk Prediction Dashboard

Full-stack web application for real-time flood risk prediction using a high-performance XGBoost model trained on All-India datasets.

## Model V3 Upgrade (Latest)
The system has been upgraded to **Model V3**, featuring:
- **Satellite Integration**: Real-time soil moisture from **NASA POWER API** (GEOS-5/SMAP).
- **Advanced ML**: High-accuracy **XGBoost** model replacing the legacy Random Forest.
- **52 Features**: Comprehensive feature engineering including rainfall acceleration, SMAP history, and geographic risk indices (TWI, CN).

## Features
- **Real-time Satellite & Weather Data**: Combines Open-Meteo precipitation with NASA's satellite soil wetness data.
- **4-Tier Risk Classification**: Low, Moderate, High, and Very High risk levels with professional iconography and alerts.
- **Model Metrics Dashboard**: Live performance indicators (AUC: 0.962, F1: 0.50) displayed on the user dashboard.
- **Modern UI**: Professional dark-themed dashboard with dynamic risk scales and interactive map integration.

---

## Project Structure

```
FloodRiskPredictor/
├── backend/
│   ├── app.py                 # Flask API server
│   ├── model_loader.py        # ML model management (V3 support)
│   ├── weather_fetcher.py     # Weather & NASA API integration 
│   ├── feature_engineering_v3.py # 52-feature engineering pipeline
│   └── requirements.txt       # Python dependencies
├── models/
│   └── new_model/             # Model V3 weights and scalers
├── frontend/
│   ├── src/
│   │   ├── components/        # React components (Dashboard, Alerts, etc.)
│   │   ├── utils/             # API client
│   │   └── App.css            # Styles with 4-tier risk themes
└── README.md
```

---

## Quick Start

### Prerequisites

- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend Setup

```bash
# Navigate to backend directory
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Run Flask server
python app.py
```

Backend will run on `http://localhost:5000`

### Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend will run on `http://localhost:3000`

---

## API Endpoints

### POST /predict
Predict flood risk for a city using Model V3 (52 features).

**Request:**
```json
{
  "city": "Patna"
}
```

**Response:**
```json
{
  "city": "Patna",
  "temperature": 28.5,
  "confidence": 87.5,
  "risk_level": "very_high",
  "risk_tier": 4,
  "model_version": "v3",
  "model_metrics": { "auc": 0.9623, "f1": 0.5032 }
}
```

### GET /cities
Get list of available cities.

### GET /health
Check server and model status.

---

## Supported Cities

| City | Latitude | Longitude |
|------|----------|-----------|
| Patna | 25.5941°N | 85.1376°E |
| Guwahati | 26.1445°N | 91.7362°E |
| Gorakhpur | 26.7606°N | 83.3732°E |
| Malda | 25.0104°N | 88.1328°E |
| ...And 20+ more major Indian cities | | |

---

## Technology Stack

**Backend:**
- **Flask** - API Framework
- **XGBoost** - Primary Machine Learning Model
- **NASA POWER API** - Satellite Soil Moisture (GWETROOT)
- **Open-Meteo API** - Current and Historical Rainfall

**Frontend:**
- **React 18** - UI Library (Vite based)
- **Axios** - Data fetching
- **Modern CSS** - 4-tier risk styling and animations

---

## ML Model (V3)

- **Algorithm**: XGBoost (Extreme Gradient Boosting)
- **Feature Count**: 52
- **Metrics**: 0.9623 AUC, 0.496 MCC
- **Critical Features**: SMAP 7-day Avg, Rainfall Acceleration, Soil Moisture Proxy, Topographic Wetness Index (TWI).

---

## Usage

1. **Select City**: Choose from the dropdown to start live analysis.
2. **View Metrics**: Click the "Model Performance" panel to see live model accuracy stats.
3. **Monitor Alerts**: High and Very High risk alerts provide actionable emergency text.

---

## Production Deployment

### Backend (Python)

```bash
# Install Gunicorn
pip install gunicorn

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Frontend (React)

```bash
# Build for production
npm run build

# Serve static files with any web server
# dist/ folder contains built files
```

**Environment Variables:**
Update API endpoint in `frontend/src/utils/api.js` to production URL.

---

## Security Notes

- Add rate limiting for API endpoints
- Implement API key authentication for production
- Use HTTPS in production
- Add input validation and sanitization

---

## Future Enhancements

- [ ] Multi-city monitoring dashboard
- [ ] Historical flood data visualization
- [ ] Email/SMS alerts for high risk
- [ ] Map-based city selection
- [ ] User authentication
- [ ] Prediction history tracking

---

## License

This project is for educational and research purposes.

---

## Contributing

Contributions welcome! Please open an issue or submit a pull request.

---

## Support

For issues or questions, please open a GitHub issue.

---

**Built for flood risk awareness and prevention**
