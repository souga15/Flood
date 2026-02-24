
from flask import Flask, request, jsonify
from flask_cors import CORS
from model_loader import get_predictor
from weather_fetcher import get_weather_for_city
import traceback
import sys
import os

# Configure Flask
app = Flask(__name__)

# CORS: allow Vercel frontend in production, localhost in dev
frontend_url = os.getenv("FRONTEND_URL", "*")
CORS(app, origins=[frontend_url, "http://localhost:3000", "http://localhost:5173"])

print("--- Starting Flood Risk Prediction API ---")

# Initialize Logic
try:
    predictor = get_predictor()
except Exception as e:
    print(f"CRITICAL: Failed to load ML models. {e}")
    sys.exit(1)

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "service": "Flood Risk Prediction API",
        "version": predictor.model_version,
        "status": "running",
        "endpoints": {
            "/health": "GET - Health check",
            "/predict": "POST - Predict flood risk (JSON: {\"city\": \"Patna\"})",
            "/cities": "GET - List available cities"
        }
    })

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "service": "flood-risk-api"})

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        if not data or 'city' not in data:
            return jsonify({"error": "City is required"}), 400
            
        city = data['city']
        print(f"Request received for: {city}")
        
        # 1. Fetch Real-time Weather
        weather_data = get_weather_for_city(city)
        print("Weather data fetched successfully")
        
        # 2. Run Prediction
        prediction = predictor.predict(city, weather_data)
        
        # 3. Construct Response
        response = {
            "city": city,
            "latitude": weather_data['latitude'],
            "longitude": weather_data['longitude'],
            "temperature": weather_data['temperature'],
            "rainfall": weather_data['rainfall'],
            "windspeed": weather_data['windspeed'],
            "humidity": weather_data['humidity'],
            "prediction": prediction['prediction'],
            "risk_level": prediction['risk_level'],
            "confidence": prediction['confidence'],
            "model_version": prediction.get('model_version', 'unknown'),
            "feature_count": prediction.get('feature_count', 0)
        }

        # Add feature explanations
        if 'feature_explanations' in prediction:
            response['feature_explanations'] = prediction['feature_explanations']
        
        if 'feature_count' in prediction:
            response['feature_count'] = prediction['feature_count']
        
        # Add model details if available (V1 includes this)
        if 'details' in prediction:
            response['model_details'] = prediction['details']
        
        return jsonify(response)

    except Exception as e:
        print(f"Error processing request: {e}")
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@app.route('/cities', methods=['GET'])
def cities():
    from weather_fetcher import CITY_COORDINATES
    return jsonify({"cities": list(CITY_COORDINATES.keys())})

if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
