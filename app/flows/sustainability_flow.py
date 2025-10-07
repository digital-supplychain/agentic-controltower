from crewai import Task
from crewai.flow.flow import Flow, listen, start
from app.utils.config import get_prompts_config
from app.data_models.sustainability_report_models import SustainabilityReport, EvaluationSection

prompts = get_prompts_config()['sustainability_flow']

class SustainabilityEvaluationFlow(Flow):
    """
    A stateful flow that evaluates a proposed supply chain action.
    The agent that executes the tasks is passed in at runtime.
    """

    @start
    def start_evaluation(self, proposed_action: str) -> Task:
        """Entry point for the flow. Kicks off the sustainability check."""
        self.state['proposed_action'] = proposed_action
        return Task(
            description=prompts['check_sustainability_task']['description'].format(proposed_action=proposed_action),
            expected_output=prompts['check_sustainability_task']['expected_output'],
            output_pydantic=EvaluationSection
        )

    @listen('start_evaluation')
    def check_compliance(self, output) -> Task:
        """Stores the sustainability result and kicks off the compliance check."""
        self.state['sustainability_check'] = output.pydantic
        return Task(
            description=prompts['check_compliance_task']['description'].format(proposed_action=self.state['proposed_action']),
            expected_output=prompts['check_compliance_task']['expected_output'],
            output_pydantic=EvaluationSection
        )

    @listen('check_compliance')
    def generate_report(self, output) -> Task:
        """Stores the compliance result and kicks off the final report generation."""
        self.state['compliance_check'] = output.pydantic
        
        report_context = prompts['report_context'].format(
            sustainability_check=self.state['sustainability_check'].model_dump_json(indent=2),
            compliance_check=self.state['compliance_check'].model_dump_json(indent=2)
        )
        
        return Task(
            description=f"{prompts['generate_report_task']['description']}\n{report_context}",
            expected_output=prompts['generate_report_task']['expected_output'],
            output_pydantic=SustainabilityReport
        )

# Instantiate the flow for use in the application
sustainability_flow = SustainabilityEvaluationFlow()