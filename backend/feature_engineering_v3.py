"""
Feature Engineering for ML Model V4 (All-India, 52 features)
Constructs 52 features: temporal encodings, rolling statistics,
SMAP soil-moisture proxies, hydrology indicators (CN, TWI), and
advanced interaction terms.

Feature order matches the V4 XGBoost scaler (52 inputs):
  1-11:  Temporal
  12-14: Weather basics
  15-20: Rainfall aggregates
  21-29: Rolling statistics
  30-31: Hydrology proxies
  32-34: SMAP soil-moisture proxies  ← NEW (3 features)
  35-37: Geographic
  38-44: CN & TWI
  45-52: Interaction features
"""
import numpy as np
from datetime import datetime
import math

# ── City elevation data (metres above sea level) ──────────────────────
CITY_ELEVATION = {
    # Assam
    'Guwahati': 55, 'Dhubri': 34, 'Jorhat': 116, 'Dibrugarh': 104,
    # Bihar
    'Patna': 53, 'Muzaffarpur': 60, 'Darbhanga': 52, 'Sitamarhi': 56,
    # Uttar Pradesh
    'Gorakhpur': 77, 'Varanasi': 81, 'Ballia': 65, 'Lucknow': 123, 'Prayagraj': 98,
    # West Bengal
    'Malda': 18, 'Murshidabad': 19, 'Kolkata': 9, 'Cooch Behar': 43,
    # Kerala
    'Kochi': 1, 'Idukki': 1200, 'Thiruvananthapuram': 10, 'Alappuzha': 2, 'Thrissur': 3,
    # Maharashtra
    'Mumbai': 14, 'Pune': 560, 'Kolhapur': 569, 'Sangli': 555,
    # Karnataka
    'Bangalore': 920, 'Bengaluru': 920, 'Belagavi': 751, 'Kodagu': 900,
    # Andhra Pradesh / Telangana
    'Visakhapatnam': 45, 'Hyderabad': 542, 'Vijayawada': 12,
    # Tamil Nadu
    'Chennai': 6, 'Cuddalore': 4,
    # Odisha
    'Bhubaneswar': 45, 'Rourkela': 219, 'Puri': 1,
    # Others
    'Delhi': 216, 'Haridwar': 314, 'Srinagar': 1585, 'Shimla': 2276,
    'Jaipur': 431, 'Bhopal': 527, 'Indore': 550, 'Ahmedabad': 53,
    'Guntur': 30, 'Cuttack': 27,
}

# ── SCS Curve Number (CN) ──────────────────────────────────────────────
CITY_CURVE_NUMBER = {
    'Guwahati': 78, 'Dhubri': 82, 'Jorhat': 75, 'Dibrugarh': 74,
    'Patna': 85, 'Muzaffarpur': 83, 'Darbhanga': 84, 'Sitamarhi': 82,
    'Gorakhpur': 80, 'Varanasi': 82, 'Ballia': 79, 'Lucknow': 78, 'Prayagraj': 80,
    'Malda': 81, 'Murshidabad': 80, 'Kolkata': 90, 'Cooch Behar': 78,
    'Kochi': 75, 'Idukki': 65, 'Thiruvananthapuram': 72, 'Alappuzha': 80, 'Thrissur': 74,
    'Mumbai': 92, 'Pune': 72, 'Kolhapur': 74, 'Sangli': 73,
    'Bangalore': 76, 'Bengaluru': 76, 'Belagavi': 73, 'Kodagu': 65,
    'Visakhapatnam': 78, 'Hyderabad': 80, 'Vijayawada': 82,
    'Chennai': 85, 'Cuddalore': 80,
    'Bhubaneswar': 79, 'Rourkela': 72, 'Puri': 82,
    'Delhi': 88, 'Haridwar': 70, 'Srinagar': 65, 'Shimla': 60,
    'Jaipur': 75, 'Bhopal': 74, 'Indore': 73, 'Ahmedabad': 82,
    'Guntur': 82, 'Cuttack': 83,
}

# ── Topographic Wetness Index (TWI) ──────────────────────────────────
CITY_TWI = {
    'Guwahati': 11.5, 'Dhubri': 14.0, 'Jorhat': 10.0, 'Dibrugarh': 10.5,
    'Patna': 14.5, 'Muzaffarpur': 14.0, 'Darbhanga': 15.0, 'Sitamarhi': 14.0,
    'Gorakhpur': 13.5, 'Varanasi': 13.0, 'Ballia': 13.5, 'Lucknow': 11.0, 'Prayagraj': 12.0,
    'Malda': 14.5, 'Murshidabad': 14.5, 'Kolkata': 16.0, 'Cooch Behar': 13.0,
    'Kochi': 12.0, 'Idukki': 6.0, 'Thiruvananthapuram': 10.0, 'Alappuzha': 15.0, 'Thrissur': 10.5,
    'Mumbai': 11.0, 'Pune': 8.0, 'Kolhapur': 9.0, 'Sangli': 9.5,
    'Bangalore': 8.5, 'Bengaluru': 8.5, 'Belagavi': 9.0, 'Kodagu': 7.0,
    'Visakhapatnam': 10.0, 'Hyderabad': 9.0, 'Vijayawada': 14.0,
    'Chennai': 13.0, 'Cuddalore': 13.5,
    'Bhubaneswar': 11.5, 'Rourkela': 8.5, 'Puri': 15.0,
    'Delhi': 10.0, 'Haridwar': 8.0, 'Srinagar': 7.0, 'Shimla': 5.5,
    'Jaipur': 9.0, 'Bhopal': 9.0, 'Indore': 8.5, 'Ahmedabad': 12.0,
    'Guntur': 12.5, 'Cuttack': 13.0,
}


# ─────────────────────────── helper functions ─────────────────────────

def _temporal_features(date=None):
    """8 temporal + 3 monsoon-period flags = 11 features."""
    if date is None:
        date = datetime.now()

    month = date.month
    doy   = date.timetuple().tm_yday
    woy   = date.isocalendar()[1]

    return {
        'Month':             month,
        'Day_of_Year':       doy,
        'Week_of_Year':      woy,
        'Is_Monsoon_Season': 1 if month in (6, 7, 8, 9) else 0,
        'Is_Peak_Monsoon':   1 if month in (7, 8) else 0,
        'Is_Pre_Monsoon':    1 if month in (4, 5) else 0,
        'Is_Post_Monsoon':   1 if month in (10, 11) else 0,
        'Month_Sin':         math.sin(2 * math.pi * month / 12),
        'Month_Cos':         math.cos(2 * math.pi * month / 12),
        'Day_of_Year_Sin':   math.sin(2 * math.pi * doy / 365),
        'Day_of_Year_Cos':   math.cos(2 * math.pi * doy / 365),
    }


def _rolling_rain_stats(history_7, history_30):
    """Rolling statistics for rainfall series."""
    h7  = np.array(history_7)  if history_7  else np.zeros(1)
    h30 = np.array(history_30) if history_30 else np.zeros(1)

    heavy_7   = int(np.sum(h7 > 50))
    extreme_7 = int(np.sum(h7 > 100))

    dry_streak = 0
    for val in reversed(h30):
        if val < 1.0:
            dry_streak += 1
        else:
            break

    return {
        'Rainfall_7Day_Avg':    float(np.mean(h7)),
        'Rainfall_7Day_Max':    float(np.max(h7)),
        'Rainfall_7Day_Std':    float(np.std(h7)),
        'Rainfall_30Day_Std':   float(np.std(h30)),
        'Heavy_Rain_Days_7D':   heavy_7,
        'Extreme_Rain_Days_7D': extreme_7,
        'Consecutive_Dry_Days': dry_streak,
    }


def _cn_runoff(cn, daily_rain_mm):
    """SCS-CN method: compute direct runoff Q (mm)."""
    if cn <= 0 or cn >= 100:
        return 0.0
    S  = (25400.0 / cn) - 254.0
    Ia = 0.2 * S
    P  = daily_rain_mm
    if P <= Ia:
        return 0.0
    Q = ((P - Ia) ** 2) / (P - Ia + S)
    return float(Q)


def _cn_category(cn):
    """Map CN to ordinal category: 0=low … 4=high."""
    if cn < 60: return 0
    if cn < 70: return 1
    if cn < 80: return 2
    if cn < 90: return 3
    return 4


def _twi_risk(twi):
    """Map TWI to risk score 0-4."""
    if twi < 7:  return 0
    if twi < 10: return 1
    if twi < 12: return 2
    if twi < 14: return 3
    return 4


# ────────────────────── main builder function ─────────────────────────

def build_feature_vector_v3(city, weather_data, current_date=None):
    """
    Build a 52-feature vector matching the V4 XGBoost model.

    The 3 SMAP soil-moisture features are estimated from rainfall/humidity
    because no real-time satellite API is available:
        SMAP_7Day_Avg     ≈ 0.010 × rain_7day  + 0.002 × hum_7avg  − 0.05
        SMAP_3Day_Max     ≈ 0.012 × rain_3day  + 0.002 × humidity  − 0.04
        Rain_on_Wet_Soil  = daily_rain × SMAP_7Day_Avg

    Args:
        city:         City name (str)
        weather_data: Dict from weather_fetcher.get_weather_for_city()
        current_date: Optional datetime (defaults to now)

    Returns:
        numpy array of shape (1, 52)
    """
    if current_date is None:
        current_date = datetime.now()

    # ── 1. Temporal (11) ──
    t = _temporal_features(current_date)

    # ── 2. Weather basics (3) ──
    temp     = weather_data.get('temperature', 25.0)
    humidity = weather_data.get('humidity', 50.0)
    wind     = weather_data.get('windspeed', 10.0)

    # ── 3. Rainfall aggregates (6) ──
    daily_rain = weather_data.get('rainfall', 0.0)
    rain_3day  = weather_data.get('rain_3day', 0.0)
    rain_7day  = weather_data.get('rain_7day', 0.0)
    rain_14day = weather_data.get('rain_14day', 0.0)
    rain_30day = weather_data.get('rain_30day', 0.0)
    rain_60day = weather_data.get('rain_60day', 0.0)

    # ── 4. Rolling stats (7 stats, features 21-29) ──
    rain_hist_7  = weather_data.get('daily_rain_history', [0] * 7)[-7:]
    rain_hist_30 = weather_data.get('daily_rain_history_30', rain_hist_7)[-30:]
    rs = _rolling_rain_stats(rain_hist_7, rain_hist_30)

    # ── 5. Temperature / humidity rolling (2) ──
    temp_hist = weather_data.get('daily_temp_history', [temp] * 7)[-7:]
    hum_hist  = weather_data.get('daily_humidity_history', [humidity] * 7)[-7:]
    temp_7avg = float(np.mean(temp_hist)) if temp_hist else temp
    hum_7avg  = float(np.mean(hum_hist))  if hum_hist  else humidity

    # ── 6. Hydrology proxies (2) ──
    soil_moisture_proxy   = rain_30day / (CITY_ELEVATION.get(city, 50) + 1)
    rainfall_acceleration = rain_3day / (rain_7day + 1)

    # ── 7. SMAP soil-moisture ─────────────────────────────────────────
    # If the exact NASA POWER API GWETROOT history was loaded, use it.
    # Otherwise, fallback to the physics-based proxy approximation.
    smap_history = weather_data.get('smap_history', [])
    if smap_history and len(smap_history) >= 1:
        # Use the real satellite data history
        smap_7day_avg = float(np.mean(smap_history))
        smap_3day_max = float(np.max(smap_history[-3:]))
    else:
        # Physics-based approximation
        smap_7day_avg = max(0.0, 0.010 * rain_7day  + 0.002 * hum_7avg  - 0.05)
        smap_3day_max = max(0.0, 0.012 * rain_3day  + 0.002 * humidity  - 0.04)
        
    rain_on_wet_soil = daily_rain * smap_7day_avg

    # ── 8. Geographic (3) ──
    elevation = CITY_ELEVATION.get(city, 50)
    latitude  = weather_data.get('latitude', 26.0)
    longitude = weather_data.get('longitude', 85.0)

    # ── 9. CN & TWI (6) ──
    cn  = CITY_CURVE_NUMBER.get(city, 78)
    twi = CITY_TWI.get(city, 11.0)
    cn_runoff   = _cn_runoff(cn, daily_rain)
    cn_cat      = _cn_category(cn)
    twi_risk    = _twi_risk(twi)
    cn_twi_haz  = cn_cat * twi_risk
    urban_flash = cn_runoff * twi / (elevation + 1)

    # ── 10. Interaction features (8) ──
    elev_rain_ratio   = elevation / (rain_7day + 1)
    elev_rain30_ratio = elevation / (rain_30day + 1)
    monsoon_rain      = t['Is_Monsoon_Season'] * daily_rain
    peak_monsoon_rain = t['Is_Peak_Monsoon'] * daily_rain
    hum_temp_product  = humidity * temp
    rain_hum_product  = daily_rain * humidity
    soil_monsoon      = soil_moisture_proxy * t['Is_Monsoon_Season']
    low_elev_heavy    = 1 if (elevation < 50 and daily_rain > 50) else 0

    # ── Assemble in exact column order (52 total) ─────────────────────
    features = [
        # Temporal (1-11)
        t['Month'],                     # 1
        t['Day_of_Year'],               # 2
        t['Week_of_Year'],              # 3
        t['Is_Monsoon_Season'],         # 4
        t['Is_Peak_Monsoon'],           # 5
        t['Is_Pre_Monsoon'],            # 6
        t['Is_Post_Monsoon'],           # 7
        t['Month_Sin'],                 # 8
        t['Month_Cos'],                 # 9
        t['Day_of_Year_Sin'],           # 10
        t['Day_of_Year_Cos'],           # 11
        # Weather basics (12-14)
        temp,                           # 12
        humidity,                       # 13
        wind,                           # 14
        # Rainfall aggregates (15-20)
        daily_rain,                     # 15
        rain_3day,                      # 16
        rain_7day,                      # 17
        rain_14day,                     # 18
        rain_30day,                     # 19
        rain_60day,                     # 20
        # Rolling stats (21-29)
        rs['Rainfall_7Day_Avg'],        # 21
        rs['Rainfall_7Day_Max'],        # 22
        rs['Rainfall_7Day_Std'],        # 23
        rs['Rainfall_30Day_Std'],       # 24
        temp_7avg,                      # 25
        hum_7avg,                       # 26
        rs['Heavy_Rain_Days_7D'],       # 27
        rs['Extreme_Rain_Days_7D'],     # 28
        rs['Consecutive_Dry_Days'],     # 29
        # Hydrology proxies (30-31)
        soil_moisture_proxy,            # 30
        rainfall_acceleration,          # 31
        # SMAP proxies (32-34) ← NEW
        smap_7day_avg,                  # 32  SMAP_7Day_Avg
        smap_3day_max,                  # 33  SMAP_3Day_Max
        rain_on_wet_soil,               # 34  Rain_on_Wet_Soil
        # Geographic (35-37)
        elevation,                      # 35
        latitude,                       # 36
        longitude,                      # 37
        # CN & TWI (38-44)
        cn,                             # 38
        twi,                            # 39
        cn_runoff,                      # 40
        cn_cat,                         # 41
        twi_risk,                       # 42
        cn_twi_haz,                     # 43
        urban_flash,                    # 44
        # Interaction features (45-52)
        elev_rain_ratio,                # 45
        elev_rain30_ratio,              # 46
        monsoon_rain,                   # 47
        peak_monsoon_rain,              # 48
        hum_temp_product,               # 49
        rain_hum_product,               # 50
        soil_monsoon,                   # 51
        low_elev_heavy,                 # 52
    ]

    return np.array([features])
