"""
ML Model Loader for Flood Prediction V4
Targeting the 'model' directory in Hugging Face root.
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

def classify_risk(flood_probability: float) -> dict:
    prob = float(flood_probability)
    if prob < 0.20:
        return {"risk_level": "low", "prediction": "Low Flood Risk", "tier": 1}
    elif prob < 0.40:
        return {"risk_level": "moderate", "prediction": "Moderate Flood Risk", "tier": 2}
    elif prob < 0.65:
        return {"risk_level": "high", "prediction": "High Flood Risk", "tier": 3}
    else:
        return {"risk_level": "very_high", "prediction": "Very High Flood Risk", "tier": 4}

class FloodPredictorV4:
    MODEL_METRICS = {
        "auc": 0.9623, "f1": 0.5032, "mcc": 0.496, "ap": 0.4264,
        "recall": 0.5342, "precision": 0.4756, "train_auc": 0.9987, "val_auc": 0.9534,
    }

    def __init__(self):
        self.model = None
        self.scaler = None
        self.feature_columns = None
        self.model_version = "v3"
        self.load_models()

    def load_models(self):
        try:
            # FIX: Pointing to 'model' folder in the root directory
            base_path = Path(__file__).parent / "model" / "new_model"
            print(f"Loading Model V3 from {base_path}...")

            self.model = joblib.load(base_path / "flood_prediction_model_all_india.pkl")
            self.scaler = joblib.load(base_path / "scaler_all_india.pkl")

            feature_file = base_path / "feature_columns_all_india.txt"
            with open(feature_file, "r") as f:
                self.feature_columns = [line.strip() for line in f.readlines()]

            print(f"✓ Model V3 loaded successfully")
        except Exception as e:
            print(f"✗ Error loading V3 models: {e}")
            raise e

    def predict(self, city, weather_data):
        features = build_feature_vector_v3(city, weather_data)
        features_scaled = self.scaler.transform(features)
        probabilities = self.model.predict_proba(features_scaled)[0]
        flood_probability = float(probabilities[1])

        risk = classify_risk(flood_probability)
        return {
            "prediction": risk["prediction"],
            "risk_level": risk["risk_level"],
            "risk_tier": risk["tier"],
            "confidence": round(flood_probability * 100, 2),
            "model_version": "v3",
            "feature_count": int(features.shape[1]),
            "model_metrics": self.MODEL_METRICS,
        }

# Simplified Global predictor instance
_predictor = None

def get_predictor():
    global _predictor
    if _predictor is None:
        try:
            _predictor = FloodPredictorV4()
        except Exception as e:
            print(f"FATAL: All models failed to load. {e}")
            raise e
    return _predictor
