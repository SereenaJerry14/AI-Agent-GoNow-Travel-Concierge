import requests
import os 
import json
from dotenv import load_dotenv

load_dotenv()
weather_key = os.getenv("OPENWEATHER_API_KEY")
serper_key = os.getenv("SERPER_API_KEY")

class Tools:
    """
    A container class to hold all external functions/tools used by the agents.
    All agents will call these methods via the initialized 'Tools' object.
    """
    def __init__(self):
        pass

    def get_weather_forecast(self, city: str, days: int = 3) -> str:
        """
        Gets a multi-day weather forecast summary (simulated) for the trip duration.
        NOTE: This is a simplified placeholder for a real API call (e.g., OpenWeatherMap One Call).
        """
        if not weather_key:
            return "Weather unavailable: API Key not loaded."        
            
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_key}&units=metric"   
        
        try:
            response = requests.get(url).json()
            if response.get("cod") != 200:
                 # Provide a default forecast if the current weather endpoint fails
                return f"Weather unavailable for {city}. Assuming moderate temperatures (20°C) and clear skies for packing guidance."
            
            temp = response['main']['temp']
            desc = response['weather'][0]['description']
            
        
            return f"Weather Report for {city} ({days} days): Current temperature is **{temp}°C ({desc})**. Forecast shows average highs of **{temp + 2}°C** and lows of **{temp - 5}°C**. Expect cool evenings and one day of chance rain. This is crucial for packing."

        except requests.exceptions.RequestException as e:
            return f"Weather unavailable due to connection error: {e}"

    def search_google(self, query: str) -> list:
        """Searches Google for real-time info and returns the top 3 results as a list of dicts."""
        url = "https://google.serper.dev/search"
        payload = ({"q": query})
        headers = {'X-API-KEY': serper_key, 'Content-Type': 'application/json'}
        
        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status() # Raise for bad status codes
            
            organic_results = response.json().get("organic", [])
            
            # Return structured list of the top 3 results
            structured_results = []
            for item in organic_results[:3]:
                structured_results.append({
                    "title": item.get("title", ""),
                    "snippet": item.get("snippet", ""),
                    "link": item.get("link", "")
                })
            
            return structured_results
            
        except requests.exceptions.RequestException as e:

            return [{"error": f"Search failed: {e}", "snippet": "No real-time data available."}]
