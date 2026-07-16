#TODO
"""
-nach welcher metrik optimieren ? 
"""

from zigzag import api  
import importlib.util
import traceback
import yaml
from openevolve.evaluation_result import EvaluationResult
from zigzag.api import get_hardware_performance_zigzag

from zigzag.utils import open_yaml
from zigzag.parser.mapping_validator import MappingValidator

#TODO: set correct paths

WORKLOAD_PATH = "examples/BA_zigzag/zigzag_inputs/models/alexnet.onnx"
ACCELERATOR_PATH = "examples/BA_zigzag/zigzag_inputs/hardware/aimc.yaml"


def calculate_combined_score(valid, energy, latency) -> float:
    result = valid * energy + latency * 1.5
    return result


def set_metric(valid: float, energy: float, latency: float, error_artifacts: dict[str, str]) -> EvaluationResult:    
    return EvaluationResult(
        metrics={
            "valid": valid,
            "energy": energy,
            "latency": latency,
            "combined_score": calculate_combined_score(valid, energy, latency),
        },
        artifacts=error_artifacts
    )
    

def is_valid_mapping(path: str) -> bool:
    try:
        data = open_yaml(path)
    except yaml.YAMLError:
        print("mapping is not valid")
        return False
    print("mapping is valid")
    return MappingValidator(data).validate()


def evaluate(program_path: str) -> EvaluationResult:
    print("ENTER EVALUATE")
    try:
        spec = importlib.util.spec_from_file_location("program", program_path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        func = getattr(mod, "generate_mapping")
        mapping_path = func()   #access the generated mapping with this path

        #DEBUG print generated mapping to std out
        """
        with open(program_path, "r", encoding="utf-8") as f:
            generated_code = f.read()
            print("###########################")
            print("GENERATED CODE")
            print(generated_code)
            print("###########################")
    
        """
        
        if not callable(func):
            #lazy error check TODO: if needed implement proper error handling 
            print("DEBUG: not callable Error!")
        
        if not is_valid_mapping(mapping_path):
            error_artifacts = {
            "error_type": "syntax error",
            "error_message": "mapping does not conform to zigzag mapping syntax",
            "full_traceback": traceback.format_exc(),
            "suggestion": "Ensure that mapping is valid yaml format AND correct zigzag mapping syntax."
            }
            return EvaluationResult(set_metric(0.0, 0.0, 0.0, error_artifacts))
        
        #TODO: check mapping for semantic
        
        print("#########DEBUG##########")
        print("mapping_path:")
        print(mapping_path)
        energy, latency, cme = api.get_hardware_performance_zigzag(
            WORKLOAD_PATH,
            ACCELERATOR_PATH,
            mapping_path,
            opt="latency"
            #TODO set correct paths if needed; if not neede remove parameters
            #dump_folder="outputs/{datetime}.json",
            #pickle_filename="outputs/list_of_cmes.pickle"
        )
        print("################ DEBUG ##############")
        print("ZIGZAG EVALUATOR CALLED!")
        error_artifacts = {}
        return EvaluationResult(set_metric(1.0, energy, latency, error_artifacts))


    except Exception as e:
        print(f"Evaluation failed at most basic step: {str(e)}")
        print(traceback.format_exc())

        error_artifacts = {
            "error_type": type(e).__name__,
            "error_message": str(e),
            "full_traceback": traceback.format_exc(),
            "suggestion": "Check for syntax errors in generated code."
        }
        return EvaluationResult(set_metric(0.0, 0.0, 0.0, error_artifacts))