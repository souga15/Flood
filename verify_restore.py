import joblib
import os

print("---- Verifying ML Artifacts ----")

model_path = "models/flood_prediction_model_real.pkl"
scaler_path = "models/scaler_real.pkl"
encoder_path = "models/label_encoder_real.pkl"

# Check existence
for path in [model_path, scaler_path, encoder_path]:
    if not os.path.exists(path):
        print(f"❌ Missing file: {path}")
    else:
        size = os.path.getsize(path) / (1024*1024)
        print(f"✔ Found {path} ({size:.2f} MB)")

# Try loading
try:
    model = joblib.load(model_path)
    print("✔ Model loaded successfully")
except Exception as e:
    print("❌ Model load failed:", e)

try:
    scaler = joblib.load(scaler_path)
    print("✔ Scaler loaded successfully")
except Exception as e:
    print("❌ Scaler load failed:", e)

try:
    encoder = joblib.load(encoder_path)
    print("✔ Encoder loaded successfully")
except Exception as e:
    print("❌ Encoder load failed:", e)
