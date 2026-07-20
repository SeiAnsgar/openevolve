"""
Evaluator for cinnamon task
"""


import importlib.util
import numpy as np
import traceback
from openevolve.evaluation_result import EvaluationResult

INITIAL_FUNCTION_NAME = "tba"

def calculate_combined_score() -> float:
    result = 1+1
    return result


def set_metric(valid: float, p1: float, p2: float, error_artifacts: dict[str, str]) -> EvaluationResult:    
    return EvaluationResult(
        metrics={
            "valid": valid,
            "metric_A": p1,
            "metric_B": p2,
            "combined_score": calculate_combined_score(),
        },
        artifacts=error_artifacts
    )


def evaluate(program_path: str) -> EvaluationResult:
    try:
        spec = importlib.util.spec_from_file_location("program", program_path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        func = getattr(mod, INITIAL_FUNCTION_NAME)


        #############Add evaluations steps here##############
        

    except Exception as e:
        print(f"Evaluation failed at most basic step: {str(e)}")
        print(traceback.format_exc())

        error_artifacts = {
            "error_type": type(e).__name__,
            "error_message": str(e),
            "full_traceback": traceback.format_exc(),
            "suggestion": "Check for syntax errors in generated code."
        }
        #TODO: set_metric() parameters
        return EvaluationResult(set_metric())