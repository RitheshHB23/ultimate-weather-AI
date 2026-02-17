"""
FLASK BACKEND FOR ULTIMATE WEATHER AI
======================================

This module provides REST API endpoints for the weather prediction application.
It handles:
- Location detection via IP
- 4-day weather forecast retrieval
- Rain prediction using ML
- JSON API responses for frontend
"""

from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import os
from typing import Dict, List, Optional
from dotenv import load_dotenv
import requests
import geocoder
from datetime import datetime, timedelta
import numpy as np
from sklearn.linear_model import LogisticRegression
import warnings

warnings.filterwarnings('ignore')

# ═══════════════════════════════════════════════════════════════════════════
# INITIALIZATION
# ═══════════════════════════════════════════════════════════════════════════

app = Flask(__name__, template_folder='templates')
CORS(app)  # Enable Cross-Origin Resource Sharing

load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")

OPENWEATHER_BASE_URL = "https://api.openweathermap.org/data/2.5"
FORECAST_URL = f"{OPENWEATHER_BASE_URL}/forecast"

# ═══════════════════════════════════════════════════════════════════════════
# LOCATION SERVICE
# ═══════════════════════════════════════════════════════════════════════════

def get_location_from_ip() -> Optional[Dict]:
    """
    Detect user location via IP address.
    
    Returns:
        Dict with city, latitude, longitude or None if detection fails
    """
    try:
        g = geocoder.ip("me")
        if g and g.latlng:
            return {
                "city": g.city or "Unknown",
                "country": g.country or "Unknown",
                "lat": g.latlng[0],
                "lng": g.latlng[1]
            }
        return None
    except Exception as e:
        print(f"Location detection error: {e}")
        return None


def get_location_from_coordinates(lat: float, lng: float) -> Optional[Dict]:
    """Get location name from coordinates."""
    try:
        g = geocoder.reverse_geocode(lat, lng)
        if g:
            return {
                "city": g.city or "Unknown",
                "country": g.country or "Unknown",
                "lat": lat,
                "lng": lng
            }
        return None
    except Exception as e:
        print(f"Reverse geocoding error: {e}")
        return None


# ═══════════════════════════════════════════════════════════════════════════
# WEATHER FORECAST SERVICE
# ═══════════════════════════════════════════════════════════════════════════

def fetch_forecast(lat: float, lng: float) -> Optional[Dict]:
    """
    Fetch 5-day weather forecast from OpenWeatherMap.
    
    Args:
        lat: Latitude
        lng: Longitude
        
    Returns:
        Forecast data or None if API call fails
    """
    if not API_KEY:
        return None
    
    try:
        params = {
            "lat": lat,
            "lon": lng,
            "appid": API_KEY,
            "units": "metric",
            "cnt": 40  # 40 * 3-hour intervals = 5 days
        }
        
        response = requests.get(FORECAST_URL, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
        
    except Exception as e:
        print(f"Forecast API error: {e}")
        return None


# ═══════════════════════════════════════════════════════════════════════════
# RAIN PREDICTION MODEL
# ═══════════════════════════════════════════════════════════════════════════

def train_rain_prediction_model() -> LogisticRegression:
    """
    Train a Logistic Regression model to predict rain.
    
    Features:
    - Humidity (%)
    - Cloud coverage (%)
    - Pressure (hPa)
    - Wind speed (m/s)
    
    Returns:
        Trained LogisticRegression model
    """
    # Synthetic training data
    X_train = np.array([
        [80, 90, 1005, 5],    # High humidity, cloudy, low pressure = RAIN
        [75, 85, 1008, 4],    # Similar conditions = RAIN
        [70, 75, 1010, 3],    # Medium conditions = RAIN
        [30, 20, 1020, 2],    # Low humidity, clear = NO RAIN
        [25, 15, 1022, 1],    # Similar conditions = NO RAIN
        [35, 25, 1018, 2],    # Similar conditions = NO RAIN
        [85, 95, 1000, 6],    # Extreme conditions = RAIN
        [20, 10, 1025, 1],    # Optimal clear = NO RAIN
        [65, 60, 1012, 3],    # Medium = Maybe RAIN
        [90, 100, 995, 8],    # Extreme = RAIN
    ])
    
    # Rain labels (1 = will rain, 0 = won't rain)
    y_train = np.array([1, 1, 1, 0, 0, 0, 1, 0, 1, 1])
    
    model = LogisticRegression(random_state=42)
    model.fit(X_train, y_train)
    return model


def predict_rain_probability(
    model: LogisticRegression,
    humidity: float,
    cloudiness: float,
    pressure: float,
    wind_speed: float
) -> float:
    """
    Predict rain probability (0-100%).
    
    Args:
        model: Trained LogisticRegression model
        humidity: Humidity percentage
        cloudiness: Cloud coverage percentage
        pressure: Atmospheric pressure (hPa)
        wind_speed: Wind speed (m/s)
        
    Returns:
        Rain probability (0-100%)
    """
    X_input = np.array([[humidity, cloudiness, pressure, wind_speed]])
    probability = model.predict_proba(X_input)[0][1] * 100
    return round(probability, 1)


# ═══════════════════════════════════════════════════════════════════════════
# DATA PROCESSING
# ═══════════════════════════════════════════════════════════════════════════

def process_forecast_data(forecast_data: Dict) -> List[Dict]:
    """
    Process forecast data into daily summaries.
    
    Args:
        forecast_data: Raw forecast from API
        
    Returns:
        List of daily forecast summaries (next 4 days)
    """
    if not forecast_data or "list" not in forecast_data:
        return []
    
    model = train_rain_prediction_model()
    daily_forecasts = {}
    
    # Group by date
    for item in forecast_data["list"]:
        date = datetime.fromtimestamp(item["dt"]).date()
        date_str = str(date)
        
        if date_str not in daily_forecasts:
            daily_forecasts[date_str] = {
                "date": date_str,
                "temps": [],
                "humidities": [],
                "cloud_cover": [],
                "pressures": [],
                "wind_speeds": [],
                "descriptions": [],
                "icons": []
            }
        
        daily_forecasts[date_str]["temps"].append(item["main"]["temp"])
        daily_forecasts[date_str]["humidities"].append(item["main"]["humidity"])
        daily_forecasts[date_str]["cloud_cover"].append(item["clouds"]["all"])
        daily_forecasts[date_str]["pressures"].append(item["main"]["pressure"])
        daily_forecasts[date_str]["wind_speeds"].append(item["wind"]["speed"])
        daily_forecasts[date_str]["descriptions"].append(item["weather"][0]["main"])
        daily_forecasts[date_str]["icons"].append(item["weather"][0]["icon"])
    
    # Create summary for next 4 days
    result = []
    today = datetime.now().date()
    
    for i in range(1, 5):  # Next 4 days
        target_date = today + timedelta(days=i)
        date_str = str(target_date)
        
        if date_str in daily_forecasts:
            data = daily_forecasts[date_str]
            
            avg_humidity = np.mean(data["humidities"])
            avg_cloud = np.mean(data["cloud_cover"])
            avg_pressure = np.mean(data["pressures"])
            avg_wind = np.mean(data["wind_speeds"])
            
            rain_prob = predict_rain_probability(
                model, avg_humidity, avg_cloud, avg_pressure, avg_wind
            )
            
            result.append({
                "date": date_str,
                "day": target_date.strftime("%A"),
                "min_temp": round(min(data["temps"]), 1),
                "max_temp": round(max(data["temps"]), 1),
                "avg_temp": round(np.mean(data["temps"]), 1),
                "humidity": int(avg_humidity),
                "cloud_cover": int(avg_cloud),
                "wind_speed": round(avg_wind, 1),
                "condition": max(set(data["descriptions"]), key=data["descriptions"].count),
                "icon": data["icons"][0],
                "rain_probability": float(rain_prob),
                "will_rain": bool(rain_prob > 50)
            })
    
    return result


# ═══════════════════════════════════════════════════════════════════════════
# REST API ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════

@app.route("/", methods=["GET"])
def index():
    """Serve the main web dashboard."""
    return render_template("index.html")


@app.route("/api/health", methods=["GET"])
def health_check():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "service": "Ultimate Weather AI",
        "timestamp": datetime.now().isoformat()
    }), 200


@app.route("/api/forecast", methods=["GET"])
def get_forecast():
    """
    Get 4-day weather forecast with rain predictions.
    
    Query Parameters:
        lat (optional): Latitude
        lng (optional): Longitude
        
    Returns:
        JSON with location and 4-day forecast
    """
    try:
        # Get location
        lat = request.args.get("lat", type=float)
        lng = request.args.get("lng", type=float)
        
        if lat is None or lng is None:
            location = get_location_from_ip()
            if not location:
                return jsonify({"error": "Could not detect location"}), 400
        else:
            location = get_location_from_coordinates(lat, lng)
        
        if not API_KEY:
            return jsonify({"error": "API key not configured"}), 500
        
        # Fetch forecast
        forecast_data = fetch_forecast(location["lat"], location["lng"])
        if not forecast_data:
            return jsonify({"error": "Could not fetch forecast"}), 500
        
        # Process forecast
        forecast = process_forecast_data(forecast_data)
        
        return jsonify({
            "success": True,
            "location": location,
            "forecast": forecast,
            "timestamp": datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e), "success": False}), 500


@app.route("/api/location", methods=["GET"])
def get_location():
    """
    Get user's current location via IP.
    
    Returns:
        JSON with city, country, coordinates
    """
    try:
        location = get_location_from_ip()
        if not location:
            return jsonify({"error": "Could not detect location"}), 400
        
        return jsonify({
            "success": True,
            "location": location,
            "timestamp": datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e), "success": False}), 500


# ═══════════════════════════════════════════════════════════════════════════
# ERROR HANDLERS
# ═══════════════════════════════════════════════════════════════════════════

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({
        "error": "Endpoint not found",
        "path": request.path,
        "success": False
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return jsonify({
        "error": "Internal server error",
        "success": False
    }), 500


# ═══════════════════════════════════════════════════════════════════════════
# RUN APPLICATION
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("\n[*] Ultimate Weather AI Backend Starting...")
    print("[*] API Documentation:")
    print("   GET /api/health              - Health check")
    print("   GET /api/location            - Get current location")
    print("   GET /api/forecast            - Get 4-day forecast with rain prediction")
    print("   GET /api/forecast?lat=X&lng=Y - Get forecast for specific coordinates")
    print("\n[*] Server running at http://localhost:5000")
    print("[*] Frontend at http://localhost:5000\n")
    
    app.run(debug=True, host="0.0.0.0", port=5000)
