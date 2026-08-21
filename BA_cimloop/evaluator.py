"""
TODO:
accelforge beispiel durchgehen
-> unterteilung anschauen,
-struktur von mapping ansehen
- wo ist der cost-evaluator und was braucht er?
"""

import importlib.util
import traceback
from openevolve.evaluation_result import EvaluationResult


import accelforge as af
from accelforge.frontend.spec import Spec
from accelforge.model.main import evaluate_mapping
from accelforge.util.parallel import set_n_parallel_jobs
from _load_spec import get_spec #

ARCH_PATH = "my_arch.yaml"
WORKLOAD_PATH = "my_workload.yaml"
#MAPPING_PATH = "my_mapping.yaml"

BATCH_SIZE = 1

#spec = af.Spec.from_yaml("arch.yaml", "workload.yaml", "mapping.yaml")


def build_spec():
    """Baut die Spec aus Arch + Workload -- identisch zum Mapper-Skript,
    nur dass hier am Ende KEIN Mapper läuft, sondern ein Mapping
    zugewiesen wird."""
    spec = get_spec(ARCH_PATH, add_dummy_main_memory=True)
 
    workload_path = af.examples.workloads.compute_in_memory.resnet18  # eigenen Pfad einsetzen
    spec.workload = af.Workload.from_yaml(
        workload_path, top_key="workload", jinja_parse_data={"BATCH_SIZE": BATCH_SIZE}
    )
    spec.renames = af.Renames.from_yaml(
        workload_path, top_key="renames", jinja_parse_data={"BATCH_SIZE": BATCH_SIZE}
    )
    return spec


def evaluate_existing_mapping(spec, mapping_path):
    try:
        spec.mapping = af.Mapping.from_yaml(mapping_path)
        result = evaluate_mapping(spec)
        return result
    except Exception as e:
        error_artifacts = {
            "error_type": type(e).__name__,
            "error_message": str(e),
            "full_traceback": traceback.format_exc(),
            "suggestion": "mapping is not valid, look for correct syntax"
        }
        return set_metric(0.0, 0.0, 0.0, error_artifacts)
 
def set_metric(result, error_artifacts: dict[str, str]) -> EvaluationResult:    
    energy_score = result.energy()
    latency_score = result.latency()
    return EvaluationResult(
        metrics={
            #"valid": valid,
            "energy": energy_score,
            "latency": latency_score,
            "combined_score": calculate_combined_score(result),
        },
        artifacts=error_artifacts
        )

def calculate_combined_score(result) -> float:
    energy_score = result.energy()
    latency_score = result.latency()
    final_score = energy_score + latency_score
    return final_score



def evaluate(program_path: str) -> EvaluationResult:
    print("ENTER EVALUATE")
    try:
        spec = importlib.util.spec_from_file_location("program", program_path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        func = getattr(mod, "generate_mapping")
        mapping_path = func()   #access the generated mapping with this path

        try:

        except Exception as e:
        #print("#########DEBUG##########")
        #print("mapping_path:")
        #print(mapping_path)


    except Exception as e:
        print(f"Evaluation failed at most basic step: {str(e)}")
        print(traceback.format_exc())

        error_artifacts = {
            "error_type": type(e).__name__,
            "error_message": str(e),
            "full_traceback": traceback.format_exc(),
            "suggestion": "Check for syntax errors in generated code."
        }
        return set_metric(0.0, 0.0, 0.0, error_artifacts)