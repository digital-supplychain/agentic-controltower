from pydantic import BaseModel, Field
from typing import List
from .erp_models import HistoricalData

class DemandForecast(BaseModel):
    """Data model for a single, specific demand forecast."""
    product_id: str = Field(..., description="The unique identifier of the product being forecasted.")
    quantity: int = Field(..., description="The forecasted demand quantity in units.")
    period: int = Field(..., description="The future time period for which this forecast is valid.")

class DemandForecastOutput(BaseModel):
    """
    Defines the final, structured output of the Demand Forecast Agent.
    This model ensures the agent's output is consistent and contains all necessary components.
    """
    historical_data: List[HistoricalData] = Field(..., description="The historical data used for the forecast.")
    risk_assessment: str = Field(..., description="The risk assessment from the Disruption Management Agent.")
    demand_forecast: DemandForecast = Field(..., description="The final demand forecast.")