from crewai_tools import MCPServerAdapter
from mcp import StdioServerParameters
from app.tools import get_digital_twin_tools as get_dt_tools

def get_erp_tools() -> list:
    """
    Factory function to create and return tools for interacting with the ERP MCP server.
    The ERP server is a stateful SSE server.
    """
    erp_params = {
        "url": "http://localhost:8000/sse",
        "transport": "sse"
    }
    return MCPServerAdapter(erp_params, connect_timeout=60).tools

def get_weather_tools() -> list:
    """
    Factory function to create and return tools for the Weather MCP server.
    This is a stateless Stdio server that is started on demand.
    """
    weather_params = StdioServerParameters(
        command="uv",
        args=["run", "python", "app/mcp/weather_server.py"]
    )
    return MCPServerAdapter(weather_params).tools

def get_news_tools() -> list:
    """
    Factory function to create and return tools for the News MCP server.
    This is a stateless Stdio server that is started on demand.
    """
    news_params = StdioServerParameters(
        command="uv",
        args=["run", "python", "app/mcp/news_server.py"]
    )
    return MCPServerAdapter(news_params).tools

def get_digital_twin_tools() -> list:
    """
    Factory function that returns a list of all available Digital Twin tools.
    This is a convenience wrapper around the function from the digital_twin_tools module.
    """
    return get_dt_tools()