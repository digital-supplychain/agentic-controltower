from crewai.tools import BaseTool
from app.flows.sustainability_flow import sustainability_flow
from app.data_models.sustainability_report_models import SustainabilityReport


class SustainabilityEvaluationTool(BaseTool):
    name: str = "Sustainability Evaluation Tool"
    description: str = "Runs a multi-step sustainability and compliance evaluation on a proposed supply chain action."

    def _run(self, proposed_action: str) -> SustainabilityReport:
        """
        Executes the sustainability evaluation flow and returns the final report as a Pydantic object.
        """
        # Late import to prevent circular dependency
        from app.agents.sustainability_compliance_agent import sustainability_compliance_agent
        
        report: SustainabilityReport = sustainability_flow.kickoff(
            inputs={'proposed_action': proposed_action}
        )
        return report

def get_sustainability_tools():
    """Returns a list of all sustainability tools."""
    return [SustainabilityEvaluationTool()]