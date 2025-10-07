from crewai import Crew, Task
from app.agents.sustainability_compliance_agent import sustainability_compliance_agent
from app.data_models.sustainability_report_models import SustainabilityReport


def test_sustainability_flow():
    """
    Tests the Sustainability & Compliance Agent by giving it tasks that require
    it to use the Sustainability Evaluation Tool.
    """
    print("--- Running Sustainability & Compliance Agent Test ---")

    # --- Test Case 1: Successful Evaluation ---
    print("\n--- Running Test Case 1: Successful Evaluation ---")
    success_task = Task(
        description="""
        A new sourcing proposal has been submitted. Please use your evaluation tool
        to conduct a full sustainability and compliance check on the following action:
        'Source 500 units of 'hops' from our approved supplier 'EcoHops Inc.' based in Germany.'
        """,
        expected_output="The final `SustainabilityReport` object from the evaluation tool.",
        agent=sustainability_compliance_agent,
        output_pydantic=SustainabilityReport
    )

    success_crew = Crew(
        agents=[sustainability_compliance_agent],
        tasks=[success_task],
        verbose=True
    )
    success_result = success_crew.kickoff()
    success_output: SustainabilityReport = success_result.pydantic

    print("\n--- Test Case 1 Result ---")
    print(success_output.model_dump_json(indent=2))
    assert success_output.recommendation.decision == 'APPROVE', "Test Case 1 Failed: Should have been approved."
    print("\n✅ Test Case 1 Passed!")

    # --- Test Case 2: Failed Evaluation ---
    print("\n--- Running Test Case 2: Failed Evaluation (Non-Ethical Supplier) ---")
    failure_task = Task(
        description="""
        A new sourcing proposal has been submitted. Please use your evaluation tool
        to conduct a full sustainability and compliance check on the following action:
        'Source 200 units of 'barley' from a new, unlisted supplier 'Shady Grains Co.''
        """,
        expected_output="The final `SustainabilityReport` object from the evaluation tool, with a clear 'REJECT' decision.",
        agent=sustainability_compliance_agent,
        output_pydantic=SustainabilityReport
    )

    failure_crew = Crew(
        agents=[sustainability_compliance_agent],
        tasks=[failure_task],
        verbose=True
    )
    failure_result = failure_crew.kickoff()
    failure_output: SustainabilityReport = failure_result.pydantic

    print("\n--- Test Case 2 Result ---")
    print(failure_output.model_dump_json(indent=2))
    assert failure_output.recommendation.decision == 'REJECT', "Test Case 2 Failed: Should have been rejected."
    print("\n✅ Test Case 2 Passed!")

    print("\n--- All Tests Complete ---")