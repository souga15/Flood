"""
Feature Engineering for ML Model V2
Constructs 28 features including temporal encodings, rolling statistics, and interaction terms
"""
import numpy as np
from datetime import datetime
import math

# City elevation data (meters above sea level)
# City elevation data (meters above sea level)
CITY_ELEVATION = {
    # Assam
    'Guwahati': 55,
    'Dhubri': 34,
    'Jorhat': 116,

    # Bihar
    'Patna': 53,
    'Muzaffarpur': 60,
    'Darbhanga': 52,
    'Sitamarhi': 56,

    # Uttar Pradesh
    'Gorakhpur': 77,
    'Varanasi': 81,
    'Ballia': 65,
    'Lucknow': 123,
    'Prayagraj': 98,

    # West Bengal
    'Malda': 18,
    'Murshidabad': 19,
    'Kolkata': 9,

    # Kerala
    'Kochi': 1,
    'Idukki': 1200,
    'Thiruvananthapuram': 10,

    # Others
    'Bhubaneswar': 45,
    'Rourkela': 219,
    'Visakhapatnam': 45,
    'Delhi': 216,
    'Haridwar': 314,
    'Srinagar': 1585,
    'Shimla': 2276,
    'Jaipur': 431,
    'Mumbai': 14,
    'Ahmedabad': 53,
    'Pune': 560,
    'Chennai': 6,
    'Bangalore': 920,
    'Hyderabad': 542,
    'Bhopal': 527,
    'Indore': 550
}

def calculate_temporal_features(date=None):
    """Calculate temporal encoding features"""
    if date is None:
        date = datetime.now()
    
    month = date.month
    day_of_year = date.timetuple().tm_yday
    week_of_year = date.isocalendar()[1]
    
    # Cyclical encoding
    month_sin = math.sin(2 * math.pi * month / 12)
    month_cos = math.cos(2 * math.pi * month / 12)
    day_sin = math.sin(2 * math.pi * day_of_year / 365)
    day_cos = math.cos(2 * math.pi * day_of_year / 365)
    
    # Monsoon season (June-September in India)
    is_monsoon = 1 if month in [6, 7, 8, 9] else 0
    
    return {
        'Month': month,
        'Day_of_Year': day_of_year,
        'Week_of_Year': week_of_year,
        'Is_Monsoon_Season': is_monsoon,
        'Month_Sin': month_sin,
        'Month_Cos': month_cos,
        'Day_of_Year_Sin': day_sin,
        'Day_of_Year_Cos': day_cos
    }

def calculate_rolling_statistics(daily_values, include_count=False):
    """
    Calculate rolling statistics from daily time series
    
    Args:
        daily_values: List of recent values (most recent last)
        include_count: Whether to include heavy rain day count
    """
    if not daily_values:
        return {
            'avg': 0.0,
            'max': 0.0,
            'std': 0.0,
            'heavy_days': 0 if include_count else None
        }
    
    values = np.array(daily_values)
    stats = {
        'avg': float(np.mean(values)),
        'max': float(np.max(values)),
        'std': float(np.std(values))
    }
    
    if include_count:
        # Count days with heavy rain (>50mm)
        stats['heavy_days'] = int(np.sum(values > 50))
    
    return stats

def build_feature_vector_v2(city, weather_data, current_date=None):
    """
    Build complete 28-feature vector for Model V2
    
    Args:
        city: City name
        weather_data: Dict with current and historical weather
        current_date: datetime object (defaults to now)
    
    Returns:
        numpy array of shape (1, 28)
    """
    if current_date is None:
        current_date = datetime.now()
    
    # 1. Temporal features (8)
    temporal = calculate_temporal_features(current_date)
    
    # 2. Current weather (3)
    temp = weather_data.get('temperature', 25.0)
    humidity = weather_data.get('humidity', 50.0)
    wind = weather_data.get('windspeed', 10.0)
    
    # 3. Current rainfall
    daily_rain = weather_data.get('rainfall', 0.0)
    
    # 4. Historical rainfall aggregates
    rain_3day = weather_data.get('rain_3day', 0.0)
    rain_7day = weather_data.get('rain_7day', 0.0)
    rain_14day = weather_data.get('rain_14day', 0.0)
    rain_30day = weather_data.get('rain_30day', 0.0)
    
    # 5. Rolling statistics for rainfall
    # Assume weather_data contains 'daily_rain_history' as list
    rain_history = weather_data.get('daily_rain_history', [0] * 7)[-7:]
    rain_stats = calculate_rolling_statistics(rain_history, include_count=True)
    
    # 6. Rolling statistics for temperature and humidity
    temp_history = weather_data.get('daily_temp_history', [temp] * 7)[-7:]
    humidity_history = weather_data.get('daily_humidity_history', [humidity] * 7)[-7:]
    
    temp_7day_avg = np.mean(temp_history) if temp_history else temp
    humidity_7day_avg = np.mean(humidity_history) if humidity_history else humidity
    
    # 7. Geographic features
    elevation = CITY_ELEVATION.get(city, 50)  # Default 50m if unknown
    latitude = weather_data.get('latitude', 26.0)
    longitude = weather_data.get('longitude', 85.0)
    
    # 8. Interaction features
    monsoon_rain_interaction = temporal['Is_Monsoon_Season'] * daily_rain
    humidity_temp_product = humidity * temp
    elevation_rain_ratio = elevation / (rain_7day + 1)  # Add 1 to avoid division by zero
    
    # Build feature array in exact order from feature_columns_v2.txt
    features = [
        temporal['Month'],                    # 1
        temporal['Day_of_Year'],              # 2
        temporal['Week_of_Year'],             # 3
        temporal['Is_Monsoon_Season'],        # 4
        temporal['Month_Sin'],                # 5
        temporal['Month_Cos'],                # 6
        temporal['Day_of_Year_Sin'],          # 7
        temporal['Day_of_Year_Cos'],          # 8
        temp,                                 # 9
        humidity,                             # 10
        wind,                                 # 11
        daily_rain,                           # 12
        rain_3day,                            # 13
        rain_7day,                            # 14
        rain_14day,                           # 15
        rain_30day,                           # 16
        rain_stats['avg'],                    # 17 - Rainfall_7Day_Avg
        rain_stats['max'],                    # 18 - Rainfall_7Day_Max
        rain_stats['std'],                    # 19 - Rainfall_7Day_Std
        elevation,                            # 20
        latitude,                             # 21
        longitude,                            # 22
        temp_7day_avg,                        # 23
        humidity_7day_avg,                    # 24
        elevation_rain_ratio,                 # 25
        monsoon_rain_interaction,             # 26
        humidity_temp_product,                # 27
        rain_stats['heavy_days']              # 28 - Heavy_Rain_Days_7D
    ]
    
    return np.array([features])
