import json
import random
from mcp.server.fastmcp import FastMCP

# This server simulates a basic news feed service.
mcp = FastMCP("News")

NEWS_HEADLINES = {
    "geopolitics": [
        "New trade tariffs announced on imported goods.",
        "Political instability reported in key shipping region.",
        "Trade agreement negotiations reach a stalemate.",
    ],
    "logistics": [
        "Port workers' strike enters third week, causing major delays.",
        "New regulations on truck driver hours expected to impact delivery times.",
        "Fuel prices surge, increasing transportation costs.",
    ],
    "default": [
        "No major disruptions reported today."
    ]
}

@mcp.tool()
def get_latest_news(topic: str) -> str:
    """Returns mock news headlines for a given topic."""
    headlines = NEWS_HEADLINES.get(topic.lower(), NEWS_HEADLINES["default"])
    selected_headline = random.choice(headlines)
    
    response = {
        "topic": topic,
        "headline": selected_headline
    }
    return json.dumps(response, indent=2)

if __name__ == "__main__":
    mcp.run()