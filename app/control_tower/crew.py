# This script assembles the complete Agentic Supply Chain Control Tower crew.
from crewai import Crew, Process

# Import utility to get the configured LLM
from app.utils.llm_utils import get_llm

# Import the specialized agents that form the workforce
from app.control_tower.crew_manager_agent import manager_agent
from app.agents.demand_forecast_agent import demand_forecast_agent
from app.agents.procurement_agent import procurement_agent
from app.agents.supplier_evaluation_agent import supplier_evaluation_agent
from app.agents.production_scheduling_agent import production_scheduling_agent
from app.agents.logistics_agent import logistics_agent
from app.agents.customer_behavior_agent import customer_behavior_agent
from app.agents.disruption_management_agent import disruption_management_agent
from app.agents.sustainability_compliance_agent import sustainability_compliance_agent
from app.agents.feedback_learning_agent import feedback_learning_agent
from app.agents.inventory_optimization_agent import inventory_optimization_agent

# Initialize the language model
llm = get_llm()

# Define and configure the main control tower crew
control_tower_crew = Crew(
    agents=[
        # List all the specialized agents that are part of this crew
        demand_forecast_agent,
        inventory_optimization_agent,
        procurement_agent,
        supplier_evaluation_agent,
        production_scheduling_agent,
        logistics_agent,
        customer_behavior_agent,
        disruption_management_agent,
        sustainability_compliance_agent,
        feedback_learning_agent,
    ],
    tasks=[],  # Tasks are defined dynamically at runtime
    process=Process.hierarchical,  # Use a hierarchical process where the manager delegates tasks
    verbose=True,
    manager_llm=llm,  # The manager agent will use the main LLM
    manager_agent=manager_agent  # Assign the pre-configured manager agent
)