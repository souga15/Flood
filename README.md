# Flood Risk Prediction Dashboard

Full-stack web application for real-time flood risk prediction using machine learning.

## 🌊 Features

- **Real-time Weather Data**: Fetches live weather from Open-Meteo API
- **ML Predictions**: Uses trained Random Forest model for flood risk assessment
- **4 Cities**: Patna, Guwahati, Gorakhpur, Malda
- **Color-coded Alerts**: Red (High Risk) / Green (Low Risk)
- **Modern UI**: Clean, responsive dashboard with gradient themes

---

## 📁 Project Structure

```
FloodRiskPredictor/
├── backend/
│   ├── app.py                 # Flask API server
│   ├── model_loader.py        # ML model management
│   ├── weather_fetcher.py     # Weather API integration
│   ├── requirements.txt       # Python dependencies
│   └── .env.example           # Environment variables template
├── models/
│   ├── flood_prediction_model_real.pkl  # Trained ML model
│   └── scaler_real.pkl                   # Feature scaler
├── frontend/
│   ├── src/
│   │   ├── components/        # React components
│   │   ├── utils/             # API client
│   │   ├── App.jsx
│   │   └── App.css
│   ├── package.json
│   └── vite.config.js
└── README.md
```

---

## 🚀 Quick Start

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

## 🔧 API Endpoints

### POST /predict
Predict flood risk for a city.

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
  "rainfall": 12.3,
  "windspeed": 15.2,
  "prediction": "High Flood Risk",
  "risk_level": "high",
  "confidence": 87.5
}
```

### GET /cities
Get list of available cities.

### GET /health
Check server and model status.

---

## 🌍 Supported Cities

| City | Latitude | Longitude |
|------|----------|-----------|
| Patna | 25.5941°N | 85.1376°E |
| Guwahati | 26.1445°N | 91.7362°E |
| Gorakhpur | 26.7606°N | 83.3732°E |
| Malda | 25.0104°N | 88.1328°E |

---

## 🛠️ Technology Stack

**Backend:**
- Flask - Web framework
- scikit-learn - ML model
- requests - HTTP client
- Flask-CORS - Cross-origin support

**Frontend:**
- React 18 - UI library
- Vite - Build tool
- Axios - HTTP client
- Modern CSS - Styling

**APIs:**
- Open-Meteo - Weather data

---

## 📊 ML Model

- **Algorithm**: Random Forest Classifier
- **Features**: Temperature, Rainfall, Wind Speed
- **Output**: Binary classification (High/Low Risk)
- **Files**:
  - `flood_prediction_model_real.pkl` (9.3 MB)
  - `scaler_real.pkl` (1.4 KB)

---

## 🎨 Usage

1. **Select City**: Choose from dropdown (Patna, Guwahati, Gorakhpur, Malda)
2. **View Weather**: See real-time temperature, rainfall, windspeed
3. **Check Risk**: Color-coded prediction displays instantly
4. **Refresh**: Click refresh button for latest data

---

## 🚢 Production Deployment

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

## 🔒 Security Notes

- Add rate limiting for API endpoints
- Implement API key authentication for production
- Use HTTPS in production
- Add input validation and sanitization

---

## 🚧 Future Enhancements

- [ ] Multi-city monitoring dashboard
- [ ] Historical flood data visualization
- [ ] Email/SMS alerts for high risk
- [ ] Map-based city selection
- [ ] User authentication
- [ ] Prediction history tracking

---

## 📝 License

This project is for educational and research purposes.

---

## 🤝 Contributing

Contributions welcome! Please open an issue or submit a pull request.

---

## 📧 Support

For issues or questions, please open a GitHub issue.

---

**Built with ❤️ for flood risk awareness and prevention**
