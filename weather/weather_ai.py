"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    ULTIMATE WEATHER AI PREDICTOR                             ║
║                   Real-Time Weather & AI Predictions                         ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import os
from typing import Optional, Dict, Tuple
import requests
from dotenv import load_dotenv
import geocoder
from sklearn.linear_model import LinearRegression
import numpy as np
from datetime import datetime

# ═══════════════════════════════════════════════════════════════════════════
# CONFIGURATION & CONSTANTS
# ═══════════════════════════════════════════════════════════════════════════

OPENWEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"
load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")


# ═══════════════════════════════════════════════════════════════════════════
# LOCATION DETECTION
# ═══════════════════════════════════════════════════════════════════════════

def get_user_location() -> Optional[Tuple[str, float, float]]:
    """
    Detect the user's current location via IP address using geocoder.
    
    Returns:
        Tuple of (city_name, latitude, longitude) or None if detection fails
        
    Raises:
        Exception: If geocoder fails to determine location
    """
    try:
        print("[*] Detecting your location via IP address...")
        g = geocoder.ip("me")
        
        if g and g.latlng:
            city = g.city or "Unknown City"
            lat, lng = g.latlng
            print(f"   [OK] Location detected: {city} ({lat:.2f}°, {lng:.2f}°)")
            return city, lat, lng
        else:
            print("   [ERR] Could not determine location via IP.")
            return None
    except Exception as e:
        print(f"   [ERR] Location detection error: {e}")
        return None


# ═══════════════════════════════════════════════════════════════════════════
# WEATHER DATA RETRIEVAL
# ═══════════════════════════════════════════════════════════════════════════

def fetch_weather_data(lat: float, lng: float) -> Optional[Dict]:
    """
    Fetch real-time weather data from OpenWeatherMap API.
    
    Args:
        lat: Latitude of the location
        lng: Longitude of the location
        
    Returns:
        Dictionary containing weather data or None if API call fails
        
    Raises:
        requests.RequestException: If API call fails
    """
    if not API_KEY:
        print("   ✗ ERROR: OPENWEATHER_API_KEY not found in .env file!")
        print("   Please create a .env file with your API key. See instructions above.")
        return None
    
    try:
        print("\n[*] Fetching real-time weather data...")
        params = {
            "lat": lat,
            "lon": lng,
            "appid": API_KEY,
            "units": "metric"  # Use Celsius; change to "imperial" for Fahrenheit
        }
        
        response = requests.get(OPENWEATHER_URL, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        print("   [OK] Weather data received successfully")
        return data
        
    except requests.exceptions.Timeout:
        print("   [ERR] API request timed out. Check your internet connection.")
        return None
    except requests.exceptions.ConnectionError:
        print("   [ERR] Connection error. Check your internet connection.")
        return None
    except requests.exceptions.HTTPError as e:
        if response.status_code == 401:
            print("   [ERR] Invalid API key. Check your .env file.")
        else:
            print(f"   [ERR] API Error {response.status_code}: {e}")
        return None
    except Exception as e:
        print(f"   [ERR] Unexpected error fetching weather: {e}")
        return None


# ═══════════════════════════════════════════════════════════════════════════
# AI MODEL - LINEAR REGRESSION
# ═══════════════════════════════════════════════════════════════════════════

def train_prediction_model() -> LinearRegression:
    """
    Train a Linear Regression model using synthetic training data.
    
    The model predicts "feels_like" temperature based on:
      - humidity (%)
      - actual temperature (C)
    
    Returns:
        Trained scikit-learn LinearRegression model
    """
    print("\n[*] Training AI model...")
    
    # Synthetic training data (humidity, temp) -> feels_like relationship
    # In real-world scenarios, this would come from historical data
    training_humidity = np.array([
        30, 40, 50, 60, 70, 80, 90,
        35, 45, 55, 65, 75, 85, 95
    ])
    
    training_temp = np.array([
        15, 18, 20, 22, 25, 28, 30,
        10, 12, 14, 16, 18, 20, 22
    ])
    
    # Feels like is influenced by both humidity and temperature
    # Higher humidity makes it feel hotter; lower humidity makes it feel cooler
    training_feels_like = (
        training_temp * 0.9 +  # Temperature coefficient
        (training_humidity / 100) * 3  # Humidity coefficient
    )
    
    # Reshape for scikit-learn (n_samples, n_features)
    X = np.column_stack((training_humidity, training_temp))
    y = training_feels_like
    
    # Train the model
    model = LinearRegression()
    model.fit(X, y)
    
    print("   [OK] AI model trained successfully")
    return model


def predict_feels_like(
    model: LinearRegression,
    humidity: float,
    temperature: float
) -> float:
    """
    Predict the "feels like" temperature using the trained AI model.
    
    Args:
        model: Trained LinearRegression model
        humidity: Current humidity percentage (0-100)
        temperature: Current temperature in Celsius
        
    Returns:
        Predicted "feels like" temperature
    """
    X_input = np.array([[humidity, temperature]])
    prediction = model.predict(X_input)[0]
    return round(prediction, 2)


# ═══════════════════════════════════════════════════════════════════════════
# DATA PROCESSING & DISPLAY
# ═══════════════════════════════════════════════════════════════════════════

def extract_weather_info(data: Dict) -> Dict:
    """
    Extract relevant weather information from API response.
    
    Args:
        data: Raw API response dictionary
        
    Returns:
        Dictionary with extracted weather info
    """
    try:
        weather_info = {
            "city": data.get("name", "Unknown"),
            "country": data.get("sys", {}).get("country", ""),
            "temperature": round(data["main"]["temp"], 2),
            "humidity": data["main"]["humidity"],
            "wind_speed": round(data["wind"]["speed"], 2),
            "feels_like": round(data["main"]["feels_like"], 2),
            "description": data["weather"][0]["description"].title(),
            "pressure": data["main"]["pressure"],
        }
        return weather_info
    except KeyError as e:
        print(f"   ✗ Error processing weather data: Missing key {e}")
        return {}


def display_weather_summary(
    location: str,
    weather: Dict,
    ai_prediction: float
) -> None:
    """
    Display a formatted weather summary with AI prediction.
    
    Args:
        location: User's location string
        weather: Dictionary with extracted weather information
        ai_prediction: AI model's prediction for feels_like temperature
    """
    if not weather:
        return
    
    print("\n" + "=" * 75)
    print("╔" + "═" * 73 + "╗")
    print("║" + " " * 15 + "[*] ULTIMATE WEATHER AI REPORT [*]" + " " * 24 + "║")
    print("╚" + "═" * 73 + "╝")
    print("=" * 75)
    
    # Location Info
    city_country = f"{weather['city']}, {weather['country']}"
    print(f"\n[*] Location: {city_country.upper()}")
    print(f"[*] Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Current Weather
    print("\n[---] CURRENT WEATHER CONDITIONS [---]")
    print(f"| [TEMP]      {weather['temperature']}C")
    print(f"| [FEELS]     {weather['feels_like']}C")
    print(f"| [WIND]      {weather['wind_speed']} m/s")
    print(f"| [HUMIDITY]  {weather['humidity']}%")
    print(f"| [PRESSURE]  {weather['pressure']} hPa")
    print(f"| [CONDITION] {weather['description']}")
    
    # AI Prediction
    difference = ai_prediction - weather['feels_like']
    symbol = "[UP]" if difference > 0 else "[DOWN]" if difference < 0 else "[SAME]"
    
    print("\n[---] AI MODEL PREDICTION [---]")
    print(f"| [AI_PRED]    {ai_prediction}C")
    print(f"| [DIFFERENCE] {symbol} {difference:+.2f}C")
    print("|")
    print("| The AI model analyzed:")
    print(f"|   * Current humidity ({weather['humidity']}%)")
    print(f"|   * Actual temperature ({weather['temperature']}C)")
    print("| ...to predict how the temperature FEELS to your body.")
    
    print("\n" + "=" * 75 + "\n")


# ═══════════════════════════════════════════════════════════════════════════
# MAIN APPLICATION FLOW
# ═══════════════════════════════════════════════════════════════════════════

def main() -> None:
    """
    Main application function that orchestrates all components.
    
    Flow:
        1. Detect user location
        2. Fetch real-time weather data
        3. Train AI prediction model
        4. Make prediction based on current conditions
        5. Display formatted summary
    """
    print("\n" + "=" * 75)
    print("[*] ULTIMATE WEATHER AI - STARTING UP...")
    print("=" * 75 + "\n")
    
    # Step 1: Get Location
    location_data = get_user_location()
    if not location_data:
        print("\n[ERROR] Failed to detect location. Please check your internet connection.")
        return
    
    city, lat, lng = location_data
    
    # Step 2: Fetch Weather Data
    weather_raw = fetch_weather_data(lat, lng)
    if not weather_raw:
        print("\n[ERROR] Failed to fetch weather data. Exiting.")
        return
    
    # Step 3: Extract Weather Info
    weather_info = extract_weather_info(weather_raw)
    
    # Step 4: Train AI Model
    model = train_prediction_model()
    
    # Step 5: Make Prediction
    ai_prediction = predict_feels_like(
        model,
        weather_info["humidity"],
        weather_info["temperature"]
    )
    
    # Step 6: Display Results
    display_weather_summary(city, weather_info, ai_prediction)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n[FATAL ERROR] {e}")
        print("Please check the error message above and review the setup instructions.")
