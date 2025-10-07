import pytest
import json
from typing import List
from app.data_models.erp_models import Product, Supplier
from mcp import ClientSession, StdioServerParameters
from mcp.client.sse import sse_client
from mcp.client.stdio import stdio_client


@pytest.mark.asyncio
async def test_mcp_servers(erp_server):
    """Tests the functionality of the ERP, Weather, and News MCP servers."""
    print("--- Testing MCP Servers ---")

    # --- Test ERP Server (SSE) ---
    print("\n--- Testing ERP Server (SSE on port 8000) ---")
    try:
        async with sse_client(url="http://localhost:8000/sse") as streams:
            async with ClientSession(*streams) as session:
                await session.initialize()
                product_info_result = await session.call_tool("get_product_info", arguments={"product_id": "beer"})
                product_info = Product(**product_info_result.structuredContent)
                print("Product Info:", product_info)
                assert product_info.name == "Premium Lager"
                assert product_info.cost == 10

                supplier_info_result = await session.call_tool("get_supplier_info", arguments={"product_id": "beer"})
                print("Raw Supplier Info Result:", supplier_info_result)
                supplier_info:list[Supplier] = [Supplier.model_validate(s) for s in supplier_info_result.structuredContent['result']]
                print("Supplier Info:", supplier_info)
                assert len(supplier_info) == 2
                assert any(s.name == "Brewery A" for s in supplier_info)
    except Exception as e:
        pytest.fail(f"ERROR connecting to ERP server: {e}")


    # --- Test Weather Server (Stdio) ---
    print("\n--- Testing Weather Server (Stdio) ---")
    weather_params = StdioServerParameters(command="uv", args=["run", "python", "app/mcp/weather_server.py"])
    try:
        async with stdio_client(weather_params) as streams:
            async with ClientSession(*streams) as session:
                await session.initialize()
                forecast = await session.call_tool("get_weather_forecast", arguments={"location": "New York"})
                print("Weather Forecast:", forecast)
    except Exception as e:
        print(f"ERROR running Weather server: {e}")

    # --- Test News Server (Stdio) ---
    print("\n--- Testing News Server (Stdio) ---")
    news_params = StdioServerParameters(command="uv", args=["run", "python", "app/mcp/news_server.py"])
    try:
        async with stdio_client(news_params) as streams:
            async with ClientSession(*streams) as session:
                await session.initialize()
                news = await session.call_tool("get_latest_news", arguments={"topic": "logistics"})
                print("Logistics News:", news)
    except Exception as e:
        print(f"ERROR running News server: {e}")
