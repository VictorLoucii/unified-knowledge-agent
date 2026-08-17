import os
import requests
from langchain_core.tools import tool

@tool
def get_weather_and_aqi(location: str) -> str:
    """
    Fetches the current weather and Air Quality Index (AQI) for a given location.
    
    Args:
        location (str): The name of the city or location (e.g., 'New Delhi', 'Vasant Kunj').
        
    Returns:
        str: A string containing the weather conditions and AQI for the requested location.
    """
    try:
        # 1. Geocoding
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={location}&count=1"
        geo_response = requests.get(geo_url)
        geo_response.raise_for_status()
        geo_data = geo_response.json()
        
        # Fallback if no results and location contains a comma
        if not geo_data.get("results") and "," in location:
            fallback_location = location.split(",")[0].strip()
            geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={fallback_location}&count=1"
            geo_response = requests.get(geo_url)
            geo_response.raise_for_status()
            geo_data = geo_response.json()
        
        if not geo_data.get("results"):
            return f"Could not find coordinates for location: {location}"
            
        lat = geo_data["results"][0]["latitude"]
        lon = geo_data["results"][0]["longitude"]
        name = geo_data["results"][0]["name"]
        
        # 2. Weather
        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        weather_response = requests.get(weather_url)
        weather_response.raise_for_status()
        weather_data = weather_response.json()
        current_weather = weather_data.get("current_weather", {})
        temp = current_weather.get("temperature", "N/A")
        windspeed = current_weather.get("windspeed", "N/A")
        
        # 3. AQI (Calculating Indian AQI from Open-Meteo raw pollutants)
        aqi_url = f"https://air-quality-api.open-meteo.com/v1/air-quality?latitude={lat}&longitude={lon}&current=pm10,pm2_5"
        aqi_response = requests.get(aqi_url)
        aqi_response.raise_for_status()
        aqi_data = aqi_response.json()
        
        current_aqi = aqi_data.get("current", {})
        pm10 = current_aqi.get("pm10", 0)
        pm25 = current_aqi.get("pm2_5", 0)
        
        def calc_sub_index(conc, breakpoints):
            if conc is None: return 0
            for (low_c, high_c, low_i, high_i) in breakpoints:
                if low_c <= conc <= high_c:
                    return ((high_i - low_i) / (high_c - low_c)) * (conc - low_c) + low_i
            return 500 if conc > breakpoints[-1][1] else 0

        pm25_bp = [(0,30,0,50), (31,60,51,100), (61,90,101,200), (91,120,201,300), (121,250,301,400), (251,1000,401,500)]
        pm10_bp = [(0,50,0,50), (51,100,51,100), (101,250,101,200), (251,350,201,300), (351,430,301,400), (431,1000,401,500)]
        
        india_aqi = max(calc_sub_index(pm25, pm25_bp), calc_sub_index(pm10, pm10_bp))
        aqi_info = f"AQI (India): {round(india_aqi)}"
            
        return f"Location: {name}\nWeather: {temp}°C, Wind Speed: {windspeed} km/h\n{aqi_info}"
        
    except Exception as e:
        return f"An error occurred while fetching weather and AQI: {str(e)}"
