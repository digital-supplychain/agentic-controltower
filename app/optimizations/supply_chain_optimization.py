import json
import subprocess
import sys
from app.data_models.optimization_models import OptimizationProblem, OptimizationResult
from app.utils.llm_utils import get_llm
from app.utils.config import get_prompts_config

class SupplyChainOptimizer:
    """
    Handles the dynamic generation and execution of the PuLP optimization model.
    """

    def solve(self, optimization_problem: OptimizationProblem) -> OptimizationResult:
        """
        Generates, executes, and parses the result of the optimization script.

        Args:
            optimization_problem: An OptimizationProblem object containing the text description of the LP problem.

        Returns:
            An OptimizationResult object with the optimal solution.

        Raises:
            RuntimeError: If the script execution or output parsing fails.
        """
        self._log_problem(optimization_problem)

        # Step 1: Use the LLM to generate the Python script from the problem description.
        script_code = self._generate_pulp_script(optimization_problem.problem_description)
        self._log_script(script_code)

        try:
            # Step 2: Execute the dynamically generated script in a sandboxed subprocess.
            # This is a critical security measure to prevent arbitrary code execution.
            result = subprocess.run(
                [sys.executable, "-c", script_code],
                capture_output=True,
                text=True,
                check=True
            )

            # Step 3: Parse the JSON output from the script's stdout.
            output = json.loads(result.stdout)
            optimization_result = OptimizationResult(**output)

            self._log_results(optimization_result)
            return optimization_result
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Error executing optimization script: {e.stderr}")
        except json.JSONDecodeError:
            raise RuntimeError(f"Error: Could not decode JSON from script output. Output was: {result.stdout}")
        except Exception as e:
            raise RuntimeError(f"An unexpected error occurred: {e}")

    def _generate_pulp_script(self, problem_description: str) -> str:
        """
        Uses an LLM to convert a natural language problem description into an executable PuLP script.

        Args:
            problem_description: A string detailing the LP problem.

        Returns:
            A string containing the executable Python script.
        """
        llm = get_llm()
        
        # Load the prompt template from the central configuration file
        prompt_template = get_prompts_config()['optimization_script_generator']['prompt_template']
        prompt = prompt_template.format(problem_description=problem_description)

        response = llm.call(prompt)

        # Sanitize the response to remove markdown code fences (e.g., ```python ... ```)
        # that LLMs sometimes add, which would cause a SyntaxError.
        if response.strip().startswith("```python"):
            response = response.strip()[9:]  # Remove ```python
            if response.strip().endswith("```"):
                response = response.strip()[:-3]
        return response.strip()

    def _log_problem(self, problem: OptimizationProblem):
        """Prints a summary of the optimization problem."""
        print("\n" + "╔" + "═" * 80 + "╗")
        print(f"║ {'AI-Generated Optimization Problem':^78} ║")
        print("╠" + "═" * 80 + "╣")
        # Wrap the text for better readability
        import textwrap
        lines = textwrap.wrap(problem.problem_description, width=76)
        for line in lines:
            print(f"║ {line:<78} ║")
        print("╚" + "═" * 80 + "╝")

    def _log_results(self, results: OptimizationResult):
        """Prints a summary of the optimization results."""
        print("\n" + "╔" + "═" * 80 + "╗")
        print(f"║ {'Optimization Results':^78} ║")
        print("╠" + "═" * 80 + "╣")
        print(f"║ Optimal Objective Value: {results.objective_value:<55.2f} ║")
        print("╟" + "─" * 80 + "╢")
        print(f"║ {'Decision Variables':^78} ║")
        print("╟" + "─" * 80 + "╢")
        for var, val in results.variable_values.items():
            print(f"║   - {var}: {val:<69.2f} ║")
        print("╚" + "═" * 80 + "╝" + "\n")

    def _log_script(self, script_code: str):
        """Prints a summary of the generated script."""
        print("\n" + "╔" + "═" * 80 + "╗")
        print(f"║ {'Dynamically Generated PuLP Script':^78} ║")
        print("╠" + "═" * 80 + "╣")
        for line in script_code.strip().split('\n'):
            print(f"║ {line:<78} ║")
        print("╚" + "═" * 80 + "╝")