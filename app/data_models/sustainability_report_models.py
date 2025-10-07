from pydantic import BaseModel, Field
from typing import List, Literal

class CheckResult(BaseModel):
    """Data model for a single sustainability or compliance check."""
    check_name: str = Field(..., description="The name of the check performed.")
    rule: str = Field(..., description="The specific rule or regulation ID being checked.")
    result: Literal['PASS', 'FAIL', 'INCOMPLETE'] = Field(..., description="The result of the check.")
    reason: str = Field(..., description="The justification for the result.")

class EvaluationSection(BaseModel):
    """Data model for a section of the evaluation (e.g., sustainability or compliance)."""
    status: Literal['PASS', 'FAIL'] = Field(..., description="The overall status of this section.")
    checks: List[CheckResult] = Field(..., description="A list of individual checks performed.")

class Recommendation(BaseModel):
    """Data model for the final recommendation."""
    decision: Literal['APPROVE', 'REJECT'] = Field(..., description="The final decision.")
    justification: str = Field(..., description="The detailed justification for the decision.")

class SustainabilityReport(BaseModel):
    """The final, structured output for the sustainability and compliance evaluation."""
    sustainability_check: EvaluationSection = Field(..., description="The results of the sustainability evaluation.")
    compliance_check: EvaluationSection = Field(..., description="The results of the compliance evaluation.")
    recommendation: Recommendation = Field(..., description="The final recommendation.")