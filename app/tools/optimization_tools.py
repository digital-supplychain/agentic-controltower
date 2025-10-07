from crewai.tools import BaseTool
from app.data_models.optimization_models import OptimizationProblem, OptimizationResult
from app.optimizations.supply_chain_optimization import SupplyChainOptimizer

class InventoryOptimizationTool(BaseTool):
    name: str = "AI-Powered Inventory Optimization Tool"
    description: str = """
    Solves a linear programming problem for inventory optimization using an AI-driven workflow.
    This tool takes a natural language description of an optimization problem, uses an LLM to
    generate a Python script to solve it, and then executes the script to find the optimal solution.
    You must provide the 'problem' as an argument, which is an OptimizationProblem object.
    """

    def _run(self, problem: OptimizationProblem) -> OptimizationResult:
        """
        Executes the AI-driven optimization process.

        Args:
            problem: An OptimizationProblem object containing the detailed text description of the LP problem.

        Returns:
            An OptimizationResult object with the optimal solution, or an error message if the process fails.
        """
        # Ensure the input is a Pydantic model, handling the case where it's passed as a dict.
        if isinstance(problem, dict):
            problem = OptimizationProblem(**problem)

        # Instantiate the optimizer and attempt to solve the problem.
        optimizer = SupplyChainOptimizer()
        try:
            result = optimizer.solve(problem)
            return result
        except RuntimeError as e:
            # Return a clear error message if any step in the optimization process fails.
            return f"Optimization failed: {e}"

def get_optimization_tools() -> list:
    """
    Factory function that returns a list of all available optimization tools.
    """
    return [InventoryOptimizationTool()]