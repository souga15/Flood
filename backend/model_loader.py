"""
ML Model Loader for Flood Prediction V3
Supports V3 (49 features, all-India), V2 (28 features), and V1 (12 features)
"""
import joblib
import numpy as np
import pandas as pd
from pathlib import Path
from datetime import datetime
import os

# Import feature engineering modules
from feature_engineering_v2 import build_feature_vector_v2
from feature_engineering_v3 import build_feature_vector_v3

class FloodPredictorV3:
    """Model V3 – All-India with 49 engineered features (incl. hydrology)"""

    def __init__(self):
        self.model = None
        self.scaler = None
        self.feature_columns = None
        self.model_version = "v3"
        self.load_models()

    def load_models(self):
        """Load V3 model, scaler, and feature list from new_model/"""
        try:
            base_path = Path(__file__).parent.parent / "models" / "new_model"
            print(f"Loading Model V3 (All-India) from {base_path}...")

            self.model = joblib.load(base_path / "flood_prediction_model_all_india.pkl")
            self.scaler = joblib.load(base_path / "scaler_all_india.pkl")

            feature_file = base_path / "feature_columns_all_india.txt"
            with open(feature_file, 'r') as f:
                self.feature_columns = [line.strip() for line in f.readlines()]

            print(f"✅ Model V3 loaded successfully")
            print(f"   Features: {len(self.feature_columns)}")
            print(f"   Model type: {type(self.model).__name__}")
        except Exception as e:
            print(f"❌ Error loading V3 models: {e}")
            raise e

    def predict(self, city, weather_data):
        """Make prediction using V3 (49-feature) engineering"""
        if self.model is None:
            raise Exception("Model not loaded")

        try:
            features = build_feature_vector_v3(city, weather_data)

            if features.shape[1] != len(self.feature_columns):
                raise ValueError(
                    f"Feature count mismatch: got {features.shape[1]}, "
                    f"expected {len(self.feature_columns)}"
                )

            print(f"DEBUG V3: Feature vector shape: {features.shape}")
            print(f"DEBUG V3: Feature sample: {features[0][:5]}...")

            features_scaled = self.scaler.transform(features)

            prediction_class = int(self.model.predict(features_scaled)[0])
            probabilities = self.model.predict_proba(features_scaled)[0]
            confidence = float(probabilities[1])

            feature_explanations = self._get_feature_importance(features[0])

            return {
                "prediction": "High Flood Risk" if prediction_class == 1 else "Low Flood Risk",
                "risk_level": "high" if prediction_class == 1 else "low",
                "confidence": round(confidence * 100, 2),
                "model_version": "v3",
                "feature_count": int(features.shape[1]),
                "feature_explanations": feature_explanations,
            }
        except Exception as e:
            print(f"ERROR in V3 prediction: {e}")
            import traceback
            traceback.print_exc()
            raise e

    def _get_feature_importance(self, feature_values):
        """Top-5 most important features with human-readable names."""
        desc = {
            'Month': 'Current month',
            'Day_of_Year': 'Day of year',
            'Week_of_Year': 'Week of year',
            'Is_Monsoon_Season': 'Monsoon season active',
            'Is_Peak_Monsoon': 'Peak monsoon (Jul-Aug)',
            'Is_Pre_Monsoon': 'Pre-monsoon (Apr-May)',
            'Is_Post_Monsoon': 'Post-monsoon (Oct-Nov)',
            'Month_Sin': 'Seasonal cycle (sin)',
            'Month_Cos': 'Seasonal cycle (cos)',
            'Day_of_Year_Sin': 'Yearly cycle (sin)',
            'Day_of_Year_Cos': 'Yearly cycle (cos)',
            'Temperature_C': 'Temperature',
            'Humidity_%': 'Humidity level',
            'Wind_Speed_kmh': 'Wind speed',
            'Daily_Rainfall_mm': 'Rainfall today',
            'Rainfall_3Day_mm': 'Rainfall (3 days)',
            'Rainfall_7Day_mm': 'Rainfall (7 days)',
            'Rainfall_14Day_mm': 'Rainfall (14 days)',
            'Rainfall_30Day_mm': 'Rainfall (30 days)',
            'Rainfall_60Day_mm': 'Rainfall (60 days)',
            'Rainfall_7Day_Avg': 'Avg daily rainfall (7d)',
            'Rainfall_7Day_Max': 'Max rainfall (7d)',
            'Rainfall_7Day_Std': 'Rainfall variability (7d)',
            'Rainfall_30Day_Std': 'Rainfall variability (30d)',
            'Temp_7Day_Avg': 'Avg temperature (7d)',
            'Humidity_7Day_Avg': 'Avg humidity (7d)',
            'Heavy_Rain_Days_7D': 'Heavy rain days (7d, >50mm)',
            'Extreme_Rain_Days_7D': 'Extreme rain days (7d, >100mm)',
            'Consecutive_Dry_Days': 'Consecutive dry days',
            'Soil_Moisture_Proxy': 'Soil moisture proxy',
            'Rainfall_Acceleration': 'Rainfall acceleration',
            'Elevation_m': 'Elevation (m)',
            'Latitude': 'Latitude',
            'Longitude': 'Longitude',
            'Curve_Number': 'SCS Curve Number (runoff)',
            'TWI': 'Topographic Wetness Index',
            'CN_Runoff_Q': 'CN direct runoff (mm)',
            'CN_Category': 'CN category',
            'TWI_Risk_Score': 'TWI risk score',
            'CN_TWI_Hazard': 'CN-TWI combined hazard',
            'Urban_Flash_Risk': 'Urban flash-flood risk',
            'Elevation_Rain_Ratio': 'Elevation-to-rain ratio (7d)',
            'Elevation_Rain30_Ratio': 'Elevation-to-rain ratio (30d)',
            'Monsoon_Rain_Interaction': 'Monsoon × rain',
            'Peak_Monsoon_Rain': 'Peak-monsoon × rain',
            'Humidity_Temp_Product': 'Humidity × temperature',
            'Rain_Humidity_Product': 'Rain × humidity',
            'Soil_Monsoon_Interaction': 'Soil-moisture × monsoon',
            'Low_Elev_Heavy_Rain': 'Low elevation + heavy rain flag',
        }

        if hasattr(self.model, 'feature_importances_'):
            importances = self.model.feature_importances_
        else:
            return []

        feature_list = []
        for idx, (name, importance) in enumerate(zip(self.feature_columns, importances)):
            if idx < len(feature_values):
                feature_list.append({
                    'name': name,
                    'description': desc.get(name, name),
                    'importance': float(importance),
                    'value': float(feature_values[idx]),
                })

        feature_list.sort(key=lambda x: x['importance'], reverse=True)
        top_5 = feature_list[:5]

        explanations = []
        for feat in top_5:
            explanations.append({
                'feature': feat['description'],
                'importance': round(feat['importance'] * 100, 1),
                'value': round(feat['value'], 2),
            })
        return explanations


class FloodPredictorV2:
    """Model V2 with 28 engineered features"""
    
    def __init__(self):
        self.model = None
        self.scaler = None
        self.feature_columns = None
        self.model_version = "v2"
        self.load_models()

    def load_models(self):
        """Load V2 model, scaler, and feature list"""
        try:
            base_path = Path(__file__).parent.parent / "models"
            
            print(f"Loading Model V2 from {base_path}...")
            
            # Load model and scaler
            self.model = joblib.load(base_path / "flood_prediction_model_v2.pkl")
            self.scaler = joblib.load(base_path / "scaler_v2.pkl")
            
            # Load feature column order
            feature_file = base_path / "feature_columns_v2.txt"
            with open(feature_file, 'r') as f:
                self.feature_columns = [line.strip() for line in f.readlines()]
            
            print(f"✅ Model V2 loaded successfully")
            print(f"   Features: {len(self.feature_columns)}")
            print(f"   Model type: {type(self.model).__name__}")
            
        except Exception as e:
            print(f"❌ Error loading V2 models: {e}")
            raise e

    def predict(self, city, weather_data):
        """Make prediction using V2 feature engineering"""
        if self.model is None:
            raise Exception("Model not loaded")

        try:
            # Build 28-feature vector using v2 feature engineering
            features = build_feature_vector_v2(city, weather_data)
            
            # Validate feature count
            if features.shape[1] != len(self.feature_columns):
                raise ValueError(f"Feature count mismatch: got {features.shape[1]}, expected {len(self.feature_columns)}")
            
            print(f"DEBUG: Feature vector shape: {features.shape}")
            print(f"DEBUG: Feature sample: {features[0][:5]}...")  # First 5 features
            
            # Scale features
            features_scaled = self.scaler.transform(features)
            
            # Predict
            prediction_class = int(self.model.predict(features_scaled)[0])
            probabilities = self.model.predict_proba(features_scaled)[0]
            confidence = float(probabilities[1])  # Probability of flood (class 1)
            
            # Extract feature importance (top 5)
            feature_explanations = self._get_feature_importance(features[0])
            
            return {
                "prediction": "High Flood Risk" if prediction_class == 1 else "Low Flood Risk",
                "risk_level": "high" if prediction_class == 1 else "low",
                "confidence": round(confidence * 100, 2),
                "model_version": "v2",
                "feature_count": int(features.shape[1]),
                "feature_explanations": feature_explanations
            }
            
        except Exception as e:
            print(f"ERROR in prediction: {e}")
            import traceback
            traceback.print_exc()
            raise e
    
    def _get_feature_importance(self, feature_values):
        """Get top 5 most important features with human-readable names"""
        # Feature name to human description mapping
        feature_descriptions = {
            'Month': 'Current month',
            'Day_of_Year': 'Day of year',
            'Week_of_Year': 'Week of year',
            'Is_Monsoon_Season': 'Monsoon season active',
            'Month_Sin': 'Seasonal cycle (sin)',
            'Month_Cos': 'Seasonal cycle (cos)',
            'Day_of_Year_Sin': 'Yearly cycle (sin)',
            'Day_of_Year_Cos': 'Yearly cycle (cos)',
            'Temperature_C': 'Temperature',
            'Humidity_%': 'Humidity level',
            'Wind_Speed_kmh': 'Wind speed',
            'Daily_Rainfall_mm': 'Rainfall today',
            'Rainfall_3Day_mm': 'Rainfall (last 3 days)',
            'Rainfall_7Day_mm': 'Rainfall (last 7 days)',
            'Rainfall_14Day_mm': 'Rainfall (last 14 days)',
            'Rainfall_30Day_mm': 'Rainfall (last 30 days)',
            'Rainfall_7Day_Avg': 'Average daily rainfall (7 days)',
            'Rainfall_7Day_Max': 'Maximum rainfall (7 days)',
            'Rainfall_7Day_Std': 'Rainfall variability (7 days)',
            'Latitude': 'Geographic latitude',
            'Longitude': 'Geographic longitude',
            'Elevation_m': 'Elevation above sea level',
            'Temp_7Day_Avg': 'Average temperature (7 days)',
            'Humidity_7Day_Avg': 'Average humidity (7 days)',
            'Monsoon_Rain_Interaction': 'Monsoon-rain combination',
            'Humidity_Temp_Product': 'Humidity-temperature factor',
            'Elevation_Rain_Ratio': 'Elevation-to-rain ratio',
            'Heavy_Rain_Days_7D': 'Heavy rain days (7 days)'
        }
        
        # Get feature importances from XGBoost model
        if hasattr(self.model, 'feature_importances_'):
            importances = self.model.feature_importances_
        else:
            # Fallback for models without feature_importances_
            return []
        
        # Create list of (feature_name, importance, value) tuples
        feature_list = []
        for idx, (name, importance) in enumerate(zip(self.feature_columns, importances)):
            if idx < len(feature_values):
                feature_list.append({
                    'name': name,
                    'description': feature_descriptions.get(name, name),
                    'importance': float(importance),
                    'value': float(feature_values[idx])
                })
        
        # Sort by importance and get top 5
        feature_list.sort(key=lambda x: x['importance'], reverse=True)
        top_5 = feature_list[:5]
        
        # Format for frontend
        explanations = []
        for feat in top_5:
            explanations.append({
                'feature': feat['description'],
                'importance': round(feat['importance'] * 100, 1),
                'value': round(feat['value'], 2)
            })
        
        return explanations


class FloodPredictorV1:
    """Legacy V1 model (12 features) - kept as fallback"""
    
    def __init__(self):
        self.model = None
        self.scaler = None
        self.label_encoder = None
        self.city_map = None
        self.model_version = "v1"
        self.load_models()

    def load_models(self):
        try:
            base_path = Path(__file__).parent.parent / "models"
            
            print(f"Loading Model V1 (fallback) from {base_path}...")
            self.model = joblib.load(base_path / "flood_prediction_model_real.pkl")
            self.scaler = joblib.load(base_path / "scaler_real.pkl")
            self.label_encoder = joblib.load(base_path / "label_encoder_real.pkl")
            
            # Build city mapping to avoid sklearn version issues
            self.city_map = {label: idx for idx, label in enumerate(self.label_encoder.classes_)}
            
            print("✅ V1 Model loaded (fallback)")
        except Exception as e:
            print(f"⚠️ Could not load V1 fallback: {e}")
            self.model = None

    def predict(self, city, weather_data):
        """V1 prediction logic (12 features)"""
        if self.model is None:
            raise Exception("V1 Model not loaded")
        
        # Use manual city encoding
        region_encoded = self.city_map.get(city, 0)
        
        current_date = datetime.now()
        month = current_date.month
        is_monsoon = 1 if month in [6, 7, 8, 9] else 0
        
        # Extract weather data  
        daily_rain = weather_data.get('rainfall', 0.0)
        rain_7 = weather_data.get('rain_7day', 0.0)
        rain_15 = weather_data.get('rain_15day', 0.0)
        rain_30 = weather_data.get('rain_30day', 0.0)
        humidity = weather_data.get('humidity', 50.0)
        temp = weather_data.get('temperature', 25.0)
        wind = weather_data.get('windspeed', 10.0)
        soil_moisture = weather_data.get('soil_moisture', 0.3)
        
        # Estimate river level
        estimated_river_level = 5.0 + (rain_30 * 0.02) + (daily_rain * 0.05)
        
        features = np.array([[
            region_encoded, month, daily_rain, rain_7, rain_15, rain_30,
            humidity, temp, estimated_river_level, soil_moisture * 100, wind, is_monsoon
        ]])
        
        features_scaled = self.scaler.transform(features)
        prediction_class = int(self.model.predict(features_scaled)[0])
        confidence = float(self.model.predict_proba(features_scaled)[0][1])
        
        return {
            "prediction": "High Flood Risk" if prediction_class == 1 else "Low Flood Risk",
            "risk_level": "high" if prediction_class == 1 else "low",
            "confidence": round(confidence * 100, 2),
            "model_version": "v1",
            "details": {
                "river_level_est": round(estimated_river_level, 2),
                "soil_moisture": round(soil_moisture * 100, 1)
            }
        }


# Global predictor instance
_predictor = None
_model_version = os.getenv("FLOOD_MODEL_VERSION", "v3")  # Default to v3

def get_predictor():
    """Get predictor instance (v3 → v2 → v1 fallback chain)"""
    global _predictor

    if _predictor is None:
        # Build ordered fallback chain based on requested version
        chain = {
            "v3": [FloodPredictorV3, FloodPredictorV2, FloodPredictorV1],
            "v2": [FloodPredictorV2, FloodPredictorV1],
            "v1": [FloodPredictorV1],
        }
        classes = chain.get(_model_version, chain["v3"])

        last_err = None
        for cls in classes:
            try:
                _predictor = cls()
                return _predictor
            except Exception as e:
                print(f"Failed to load {cls.__name__}: {e}, trying next...")
                last_err = e

        raise last_err  # all failed

    return _predictor
