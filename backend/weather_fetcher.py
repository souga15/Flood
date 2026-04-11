"""
Weather data fetcher using Open-Meteo API
"""
import requests
from typing import Dict, Tuple

# City coordinates for flood-prone regions and major cities in India
CITY_COORDINATES = {
    # Assam
    "Guwahati": (26.1445, 91.7362),
    "Dhubri": (26.0207, 89.9743),
    "Jorhat": (26.7509, 94.2037),

    # Bihar
    "Patna": (25.5941, 85.1376),
    "Muzaffarpur": (26.1209, 85.3647),
    "Darbhanga": (26.1542, 85.8918),
    "Sitamarhi": (26.5937, 85.4199),

    # Uttar Pradesh
    "Gorakhpur": (26.7606, 83.3732),
    "Varanasi": (25.3176, 82.9739),
    "Ballia": (25.7615, 84.1483),
    "Lucknow": (26.8467, 80.9462),
    "Prayagraj": (25.4358, 81.8463),

    # West Bengal
    "Malda": (25.0104, 88.1328),
    "Murshidabad": (24.1878, 88.2698),
    "Kolkata": (22.5726, 88.3639),

    # Kerala
    "Kochi": (9.9312, 76.2673),
    "Idukki": (9.8494, 76.9802),
    "Thiruvananthapuram": (8.5241, 76.9366),

    # Odisha
    "Bhubaneswar": (20.2961, 85.8245),
    "Rourkela": (22.2604, 84.8536),

    # Maharashtra
    "Mumbai": (19.0760, 72.8777),
    "Pune": (18.5204, 73.8567),

    # Karnataka
    "Bangalore": (12.9716, 77.5946),

    # Andhra Pradesh
    "Visakhapatnam": (17.6868, 83.2185),
    "Hyderabad": (17.3850, 78.4867), # Telangana/AP region

    # Tamil Nadu
    "Chennai": (13.0827, 80.2707),

    # Other North/Central
    "Delhi": (28.6139, 77.2090),
    "Haridwar": (29.9457, 78.1642),
    "Srinagar": (34.0837, 74.7973),
    "Shimla": (31.1048, 77.1734),
    "Jaipur": (26.9124, 75.7873),
    "Bhopal": (23.2599, 77.4126),
    "Indore": (22.7196, 75.8577),
    "Ahmedabad": (23.0225, 72.5714)
}

def get_city_coordinates(city_name: str) -> Tuple[float, float]:
    """
    Get latitude and longitude for a city
    
    Args:
        city_name: Name of the city
        
    Returns:
        Tuple of (latitude, longitude)
        
    Raises:
        ValueError: If city is not in the database
    """
    if city_name not in CITY_COORDINATES:
        raise ValueError(f"City '{city_name}' not found. Available cities: {list(CITY_COORDINATES.keys())}")
    
    return CITY_COORDINATES[city_name]

def fetch_weather_data(latitude: float, longitude: float) -> Dict:
    """
    Fetch current weather data from Open-Meteo API
    
    Args:
        latitude: Latitude coordinate
        longitude: Longitude coordinate
        
    Returns:
        Dictionary with weather data
        
    Raises:
        requests.RequestException: If API call fails
    """
    url = "https://api.open-meteo.com/v1/forecast"
    
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,relative_humidity_2m,wind_speed_10m,precipitation,rain,soil_moisture_0_to_1cm",
        "daily": "precipitation_sum,temperature_2m_max",
        "past_days": 60,
        "forecast_days": 1
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise Exception(f"Failed to fetch weather data: {str(e)}")

def extract_weather_features(api_response: Dict) -> Dict[str, float]:
    """
    Extract comprehensive features for ML model V2
    Now includes daily history arrays for rolling statistics
    """
    current = api_response.get("current", {})
    daily = api_response.get("daily", {})
    daily_rain = daily.get("precipitation_sum", [])
    daily_temp = daily.get("temperature_2m_max", [])  # Daily max temp
    daily_humidity = daily.get("relative_humidity_2m", [])  # If available
    
    # Current basics
    temperature = current.get("temperature_2m", 0.0)
    windspeed = current.get("wind_speed_10m", 0.0)
    humidity = current.get("relative_humidity_2m", 50.0)
    soil_moisture = current.get("soil_moisture_0_to_1cm", 0.3)
    daily_rain_current = current.get("precipitation", 0.0)

    # Prepare rain data (exclude today's forecast)
    rain_data = daily_rain[:-1] if len(daily_rain) > 1 else []
    
    def sum_last_n(data, n):
        if not data: return 0.0
        return sum(data[-n:])
    
    # Calculate all required rainfall aggregates
    rain_3day = sum_last_n(rain_data, 3)
    rain_7day = sum_last_n(rain_data, 7)
    rain_14day = sum_last_n(rain_data, 14)
    rain_15day = sum_last_n(rain_data, 15)
    rain_30day = sum_last_n(rain_data, 30)
    rain_60day = sum_last_n(rain_data, 60)
    
    # Extract daily history arrays
    daily_rain_history = list(rain_data[-7:]) if len(rain_data) >= 7 else list(rain_data)
    daily_rain_history_30 = list(rain_data[-30:]) if len(rain_data) >= 30 else list(rain_data)
    daily_temp_history = list(daily_temp[-7:]) if len(daily_temp) >= 7 else [temperature] * 7
    daily_humidity_history = [humidity] * 7  # Open-Meteo may not provide daily humidity, use current

    return {
        "temperature": float(temperature),
        "rainfall": float(daily_rain_current),
        "windspeed": float(windspeed),
        "humidity": float(humidity),
        "soil_moisture": float(soil_moisture),
        "rain_3day": float(rain_3day),
        "rain_7day": float(rain_7day),
        "rain_14day": float(rain_14day),
        "rain_15day": float(rain_15day),
        "rain_30day": float(rain_30day),
        "rain_60day": float(rain_60day),
        "daily_rain_history": daily_rain_history,
        "daily_rain_history_30": daily_rain_history_30,
        "daily_temp_history": daily_temp_history,
        "daily_humidity_history": daily_humidity_history,
    }

def fetch_nasa_smap_data(latitude: float, longitude: float) -> list:
    """
    Fetch the last 10 days of GWETROOT from NASA POWER.
    Returns a list of the most recent valid measurements.
    """
    import datetime
    end = datetime.datetime.now()
    start = end - datetime.timedelta(days=12)
    url = "https://power.larc.nasa.gov/api/temporal/daily/point"
    
    params = {
        "parameters": "GWETROOT",
        "community": "AG",
        "longitude": longitude,
        "latitude": latitude,
        "start": start.strftime("%Y%m%d"),
        "end": end.strftime("%Y%m%d"),
        "format": "JSON"
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        gwetroot = data.get('properties', {}).get('parameter', {}).get('GWETROOT', {})
        # Sort by date
        sorted_dates = sorted(gwetroot.keys())
        valid_vals = []
        for d in sorted_dates:
            val = gwetroot[d]
            if val != -999.0:  # NASA's missing value code
                valid_vals.append(val)
        # return the 7 most recent valid values
        return valid_vals[-7:] if valid_vals else []
    except Exception as e:
        print(f"Warning: Failed to fetch SMAP data: {e}")
        return []

def get_weather_for_city(city_name: str) -> Dict[str, float]:
    """
    Get expanded weather data for a specific city
    """
    lat, lon = get_city_coordinates(city_name)
    weather_data = fetch_weather_data(lat, lon)
    result = extract_weather_features(weather_data)
    
    # Fetch real NASA SMAP data
    smap_history = fetch_nasa_smap_data(lat, lon)
    result['smap_history'] = smap_history
    
    result['latitude'] = lat
    result['longitude'] = lon
    return result
