from pydantic import BaseModel, Field
from typing import List, Dict

class OptimizationProblem(BaseModel):
    """
    Defines the optimization problem as a detailed, human-readable text description.
    This allows the agent to formulate the problem abstractly before it's converted into a script.
    """
    problem_description: str = Field(..., description="A highly detailed and specific text description of the linear programming problem. This description MUST be self-contained and include: 1. The full mathematical formulation of the objective function. 2. The complete mathematical formulation of all constraints. 3. A clear definition of all decision variables and their bounds (e.g., non-negative).")

class OptimizationResult(BaseModel):
    """
    Structures the output from the AI-driven optimization process, providing the
    solution to the linear programming problem.
    """
    objective_value: float = Field(..., description="The optimal value of the objective function.")
    variable_values: Dict[str, float] = Field(..., description="A dictionary of decision variables and their optimal values.")