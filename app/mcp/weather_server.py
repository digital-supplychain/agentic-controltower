import json
import random
from mcp.server.fastmcp import FastMCP

# This server simulates a basic weather forecast service.
mcp = FastMCP("Weather")

@mcp.tool()
def get_weather_forecast(location: str) -> str:
    """Returns a mock weather forecast for a given location."""
    possible_forecasts = ["Sunny", "Cloudy", "Rain", "Heavy Rain", "Snow"]
    forecast = random.choice(possible_forecasts)
    
    response = {
        "location": location,
        "forecast": forecast
    }
    return json.dumps(response, indent=2)

if __name__ == "__main__":
    mcp.run()