# src/subagents/weather_agent.py

class WeatherAgent:
    """
    Fetches the weather forecast using the Tools class.
    """
    def __init__(self, tools):
        self.tools = tools

    def get_weather_forecast_summary(self, city: str, days: int) -> str:
        """
        Calls the tools function to get the weather summary for the trip.
        """
        # Calls the corrected method in src/tools.py
        return self.tools.get_weather_forecast(city, days)