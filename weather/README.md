# 🌍 Ultimate Weather AI Predictor

A sophisticated Python application that detects your location, fetches real-time 4-day weather forecasts, and uses machine learning to predict whether it will rain.

## 📋 Features

### 🎯 Core Features
✅ **4-Day Weather Forecast** - Predict weather for the next 4 days  
✅ **AI Rain Prediction** - Logistic Regression model predicts rain probability  
✅ **Auto Location Detection** - Uses your IP address to find your city  
✅ **Real-Time Weather Data** - Fetches current & forecast data from OpenWeatherMap API  
✅ **Secure API Key Management** - Uses `.env` file for sensitive credentials  

### 🖥️ Web Application
✅ **Beautiful Web Dashboard** - Modern, responsive UI with real-time updates  
✅ **REST API Backend** - Flask-based backend with JSON endpoints  
✅ **Interactive Frontend** - Built with HTML5, CSS3, and vanilla JavaScript  
✅ **Rain Probability Visualization** - Dynamic progress bars and indicators  

### 🛡️ Code Quality
✅ **Modular Functions** - Clean, reusable code structure  
✅ **Type Hints** - Full type annotations for better maintainability  
✅ **Robust Error Handling** - Comprehensive exception handling  
✅ **CORS Enabled** - Cross-Origin Resource Sharing for development  

---

## 🚀 Quick Start (5 Minutes)

### 1️⃣ Install Dependencies

Open your terminal in this folder and run:

```bash
pip install -r requirements.txt
```

Or manually:

```bash
pip install requests geocoder scikit-learn python-dotenv numpy flask flask-cors
```

### 2️⃣ Get Your API Key

1. Visit [OpenWeatherMap API](https://openweathermap.org/api)
2. Sign up for a **FREE** account
3. Go to your dashboard and copy your API Key

### 3️⃣ Create `.env` File

In this folder, create a file named `.env`:

```
OPENWEATHER_API_KEY=your_api_key_here
```

### 4️⃣ Run the Web Application

```bash
python app.py
```

Then open your browser to: **http://localhost:5000**

The web dashboard will show:
- 📅 4-day weather forecast
- 🌧️ AI-predicted rain probability for each day
- 📊 Temperature trends (min/avg/max)
- 💧 Humidity, cloud cover, wind speed
- 🎯 Smart rain indicators (color-coded)

---

## 📦 Project Structure

```
weather/
├── app.py                    # Flask backend (REST API)
├── weather_ai.py             # CLI version (standalone)
├── requirements.txt          # Dependencies
├── .env                      # Your API key (create this)
├── .env.example              # Example template
├── .gitignore                # Git ignore rules
├── README.md                 # This file
└── templates/
    └── index.html            # Web dashboard frontend
```

---

## 🏗️ Architecture

```
┌─────────────────────┐
│  Frontend (Browser) │
│  (HTML/CSS/JS)      │
└──────────┬──────────┘
           │
           │ HTTP/JSON
           ▼
┌─────────────────────────┐
│  Flask Backend (app.py) │
│  - REST API endpoints   │
│  - Location detection   │
│  - Forecast processing  │
│  - ML predictions       │
└──────────┬──────────────┘
           │
           │ HTTPS
           ▼
┌──────────────────────────┐
│ OpenWeatherMap API       │
│ (Real-time weather data) │
└──────────────────────────┘
```

---

## 📡 API Endpoints

The Flask backend provides these REST endpoints:

### Health Check
```
GET /api/health
```
Returns service status and timestamp.

### Get Current Location
```
GET /api/location
```
Returns: `{city, country, lat, lng}`

### Get 4-Day Forecast + Rain Prediction
```
GET /api/forecast
GET /api/forecast?lat=12.97&lng=77.59
```

Returns: 4-day forecast with:
- Temperature (min/avg/max)
- Weather condition & icon
- Humidity, cloud cover, wind speed
- **Rain probability (0-100%)**
- Boolean flag: `will_rain`

Example response:
```json
{
  "success": true,
  "location": {
    "city": "Bengaluru",
    "country": "India",
    "lat": 12.97,
    "lng": 77.59
  },
  "forecast": [
    {
      "date": "2026-02-17",
      "day": "Tuesday",
      "min_temp": 15.2,
      "avg_temp": 18.5,
      "max_temp": 22.1,
      "humidity": 72,
      "cloud_cover": 65,
      "wind_speed": 3.2,
      "condition": "Cloudy",
      "icon": "04d",
      "rain_probability": 65.3,
      "will_rain": true
    }
  ]
}
```

---

## 🤖 AI Model: Rain Prediction

### How It Works

The model uses **Logistic Regression** to predict rain probability based on:

| Feature | Range | Impact |
|---------|-------|--------|
| **Humidity** | 0-100% | Higher = More likely to rain |
| **Cloud Cover** | 0-100% | Higher = More likely to rain |
| **Pressure** | ~950-1050 hPa | Lower = More likely to rain |
| **Wind Speed** | 0-30+ m/s | Higher = More likely to rain |

### Training Data

The model learns from synthetic patterns that mimic real weather relationships:
- High humidity + low pressure + clouds = RAIN
- Low humidity + high pressure + clear = NO RAIN
- Medium conditions = Mixed predictions

### Output Interpretation

- **0-30%**: ✨ Unlikely to rain
- **30-70%**: ⚠️ Moderate rain chance
- **70-100%**: ☔ High chance of rain

---

## 🎨 Frontend Features

### Dashboard Layout

1. **Header Section**
   - Application title
   - Current location (auto-detected)
   - Refresh button

2. **Forecast Cards** (4-Day Grid)
   - Day name + date
   - Weather icon (emoji)
   - Temperature range (min/avg/max)
   - Weather condition
   - **Rain probability bar chart**
   - Rain indicator (color-coded)
   - Additional stats (humidity, clouds, wind)

3. **Color Scheme**
   - **Cyan**: Primary (healthy/info)
   - **Green**: Low rain probability
   - **Orange**: Medium rain probability
   - **Red**: High rain probability

4. **Responsive Design**
   - Works on desktop, tablet, mobile
   - Touch-friendly buttons
   - Smooth animations

---

## 🧪 Testing the Application

### Test Endpoints with curl

```bash
# Health check
curl http://localhost:5000/api/health

# Get your location
curl http://localhost:5000/api/location

# Get forecast for your location
curl http://localhost:5000/api/forecast

# Get forecast for specific coordinates
curl "http://localhost:5000/api/forecast?lat=51.5074&lng=-0.1278"
```

### Test Different Locations

Modify the API call with different coordinates:
- **London**: `lat=51.5074&lng=-0.1278`
- **New York**: `lat=40.7128&lng=-74.0060`
- **Tokyo**: `lat=35.6762&lng=139.6503`
- **Sydney**: `lat=-33.8688&lng=151.2093`

---

## 📋 Troubleshooting

### "Could not detect location"
- Check your internet connection
- Some networks block IP geolocation
- Try specifying coordinates: `?lat=X&lng=Y`

### "Could not fetch forecast"
- Verify `.env` file has correct API key
- Check OpenWeatherMap API status
- Verify internet connectivity

### Frontend not loading
- Ensure Flask backend is running: `python app.py`
- Check browser console for errors (F12)
- Verify port 5000 is not blocked

### CORS errors
- CORS is enabled in `app.py`
- Ensure you're accessing from `http://localhost:5000`
- Don't mix http/https

---

## 🎓 Learning Outcomes

This project teaches:
- ✅ Building REST APIs with Flask
- ✅ Machine Learning with scikit-learn
- ✅ Frontend development (HTML/CSS/JS)
- ✅ API integration and data processing
- ✅ Weather data analysis
- ✅ Probability prediction models
- ✅ Error handling and validation

---

## 🔐 Security Notes

1. **Never commit `.env` file**
   - It's already in `.gitignore`
   - Contains your API key

2. **Protect your API key**
   - Don't share it publicly
   - Rotate if accidentally exposed

3. **Production Deployment**
   - Use environment variables
   - Enable HTTPS
   - Add rate limiting
   - Validate all inputs

---

## 📊 Sample Output

```
🌍 Ultimate Weather AI Backend Starting...
📍 API Documentation:
   GET /api/health              - Health check
   GET /api/location            - Get current location
   GET /api/forecast            - Get 4-day forecast with rain prediction
   GET /api/forecast?lat=X&lng=Y - Get forecast for specific coordinates

🚀 Server running at http://localhost:5000
🌐 Frontend at http://localhost:5000
```

Then open **http://localhost:5000** in your browser!

---

## 📝 License

This project is open source and free to use and modify.

---

## 🤝 Support

Issues? Check:
1. `.env` file exists and has correct API key
2. All dependencies installed: `pip install -r requirements.txt`
3. Flask backend running: `python app.py`
4. Internet connectivity
5. OpenWeatherMap API status

---

**Happy Weather Predicting! 🌧️⛅🌞**


---

## 📦 Dependencies

| Package | Purpose |
|---------|---------|
| **requests** | Make HTTP requests to OpenWeatherMap API |
| **geocoder** | Detect your location via IP address |
| **scikit-learn** | Train and use the Linear Regression model |
| **python-dotenv** | Load API key from `.env` file |
| **numpy** | Numerical operations for the ML model |

---

## 🏗️ Project Structure

```
weather/
├── weather_ai.py          # Main application (fully documented)
├── .env                   # Your API key (create this)
├── .env.example           # Example template
├── README.md              # This file
└── .gitignore             # Prevents committing .env
```

---

## 🔧 How It Works

### Step-by-Step Flow

```
1. Location Detection
   └─> Uses geocoder to find your city via IP
   
2. Weather Data Retrieval
   └─> Calls OpenWeatherMap API with your coordinates
   
3. AI Model Training
   └─> Trains Linear Regression on synthetic data
       (humidity + temperature → feels_like)
   
4. Prediction
   └─> Uses current conditions to predict feels_like temp
   
5. Display Results
   └─> Shows formatted weather summary with prediction
```

### AI Model Explanation

The model predicts **"feels like"** temperature based on:

- **Humidity (0-100%)**: Higher humidity makes temperature feel hotter
- **Actual Temperature (°C)**: Base temperature input

**Formula Used:**
```
feels_like_predicted = (temp × 0.9) + (humidity / 100) × 3
```

---

## ⚠️ Important Security Notes

### 🔐 Protecting Your API Key

1. **Never commit `.env` to GitHub**
   - Add this line to `.gitignore`:
     ```
     .env
     ```

2. **Use `.env.example`** as a template for other developers

3. **Rotate keys if exposed** on GitHub:
   - Deactivate old key on OpenWeatherMap dashboard
   - Generate a new one
   - Update `.env`

---

## 🐛 Troubleshooting

### "OPENWEATHER_API_KEY not found in .env file"
- Make sure `.env` file exists in the same folder as `weather_ai.py`
- Check the file name is exactly `.env` (not `.env.txt`)
- Verify the format: `OPENWEATHER_API_KEY=your_key_here`

### "Invalid API key"
- Go to [OpenWeatherMap Dashboard](https://openweathermap.org/api)
- Copy the key again
- Paste it in `.env` file
- Make sure there are no extra spaces

### "Could not determine location via IP"
- Check your internet connection
- Try running again
- Some networks block IP geolocation

### "Connection error"
- Verify you have internet access
- Check if OpenWeatherMap API is accessible
- Try visiting their website in your browser

---

## 📊 Sample Output

```
═══════════════════════════════════════════════════════════════════════════
🌍 ULTIMATE WEATHER AI - STARTING UP...
═══════════════════════════════════════════════════════════════════════════

🔍 Detecting your location via IP address...
   ✓ Location detected: San Francisco (37.77°, -122.42°)

🌡️  Fetching real-time weather data...
   ✓ Weather data received successfully

🤖 Training AI model...
   ✓ AI model trained successfully

═════════════════════════════════════════════════════════════════════════════
╔═══════════════════════════ ⛅ ULTIMATE WEATHER AI REPORT ⛅ ═════════════════╗
╚═════════════════════════════════════════════════════════════════════════════╝
═════════════════════════════════════════════════════════════════════════════

📍 Location: SAN FRANCISCO, US
🕐 Time: 2026-02-16 14:30:45

┌─ CURRENT WEATHER CONDITIONS ─────────────────────────────────────┐
│ 🌡️  Temperature:      18.45°C                                     │
│ 🌫️  Feels Like:       16.89°C                                     │
│ 💨 Wind Speed:       4.2 m/s                                    │
│ 💧 Humidity:         72%                                        │
│ 🔽 Pressure:         1013 hPa                                   │
│ 📝 Conditions:       Partly Cloudy                              │
└─────────────────────────────────────────────────────────────────┘

┌─ AI MODEL PREDICTION ───────────────────────────────────────────┐
│ 🤖 Predicted Feels Like:  16.92°C                               │
│ ➡️ Difference from actual: +0.03°C                              │
│                                                                 │
│ The AI model analyzed:                                          │
│   • Current humidity (72%)                                      │
│   • Actual temperature (18.45°C)                                │
│ ...to predict how the temperature FEELS to your body.          │
└─────────────────────────────────────────────────────────────────┘

═════════════════════════════════════════════════════════════════════════════
```

---

## 📚 Code Features

### Modular Functions
- `get_user_location()` - Location detection
- `fetch_weather_data()` - API data retrieval
- `train_prediction_model()` - ML model training
- `predict_feels_like()` - Temperature prediction
- `extract_weather_info()` - Data processing
- `display_weather_summary()` - CLI output

### Type Hints
All functions include full type annotations for clarity:
```python
def fetch_weather_data(lat: float, lng: float) -> Optional[Dict]:
    ...
```

### Error Handling
Comprehensive try-except blocks for:
- Location detection failures
- API timeouts and connection errors
- Invalid API keys
- Missing required data fields

---

## 🎓 Learning Outcomes

This project teaches:
- ✅ Working with REST APIs (`requests`)
- ✅ IP-based geolocation (`geocoder`)
- ✅ Machine Learning basics (`scikit-learn`)
- ✅ Environment variable security (`python-dotenv`)
- ✅ Clean code practices (type hints, modular functions)
- ✅ Error handling and logging
- ✅ Data processing and formatting

---

## 📖 Further Customization

### Change Temperature Units
Edit line ~35 in `weather_ai.py`:
```python
# Change from "metric" (Celsius) to "imperial" (Fahrenheit)
"units": "imperial"
```

### Improve AI Model
Replace the synthetic training data with real historical data:
```python
# In train_prediction_model() function
training_humidity = np.array([...])  # Real historical humidity
training_temp = np.array([...])      # Real historical temperatures
training_feels_like = np.array([...]) # Real historical feels_like
```

### Add More Features
Include additional weather parameters:
- Precipitation
- UV Index
- Air Quality
- Weather alerts

---

## 📝 License

This project is open source and free to use and modify.

---

## 🤝 Support

If you encounter issues:
1. Check the **Troubleshooting** section above
2. Verify your `.env` file is correct
3. Ensure all dependencies are installed
4. Check internet connectivity

---

**Happy Weather Predicting! 🌧️⛅🌞**
