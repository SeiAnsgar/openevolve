"""
run script with:
python openevolve-run.py BA_zigzag/initial_program.py BA_zigzag/evaluator.py --config BA_zigzag/config.yaml --iterations 10
"""

#this is to prevent error messaages (caused by plotting during headless exec)
import matplotlib
matplotlib.use("Agg")

from zigzag import api  
import importlib.util
import traceback
import yaml
from openevolve.evaluation_result import EvaluationResult
from zigzag.api import get_hardware_performance_zigzag

from zigzag.utils import open_yaml
from zigzag.parser.mapping_validator import MappingValidator

#TODO: set correct paths

WORKLOAD_PATH = "BA_zigzag/zigzag_inputs/models/resnet50_infer.onnx"
ACCELERATOR_PATH = "BA_zigzag/zigzag_inputs/hardware/aimc.yaml"
DUMP_FOLDER_PATH = "BA_zigzag/zigzag_output"
PICKLE_PATH = "BA_zigzag/zigzag_output"


BASELINE_ENERGY = 18719445507
BASELINE_LATENCY = 64714023.0000

def calculate_combined_score(valid, energy, latency) -> float:
    energy_score = (BASELINE_ENERGY / (energy + 1e-6))/100
    latency_score = BASELINE_LATENCY / (latency + 1e-6)
    result = valid * 0.5 * (energy_score + latency_score)
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
        print("mapping is not NOT in yaml format")
        return False
    print("mapping is in yaml format")
    return MappingValidator(data).validate()


def evaluate(program_path: str) -> EvaluationResult:
    print("ENTER EVALUATE")
    try:
        spec = importlib.util.spec_from_file_location("program", program_path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        func = getattr(mod, "generate_mapping")
        mapping_path = func()   #access the generated mapping with this path
        
        if not callable(func):
            #TODO: if needed implement proper error handling 
            print("DEBUG: not callable Error!")
        
        if not is_valid_mapping(mapping_path):
            error_artifacts = {
            "error_type": "syntax error",
            "error_message": "mapping does not conform to zigzag mapping syntax",
            "full_traceback": traceback.format_exc(),
            "suggestion": "Ensure that mapping is valid yaml format AND correct zigzag mapping syntax."
            }
            return set_metric(0.0, 0.0, 0.0, error_artifacts)
        
        #TODO: check mapping for semantic
        
        #print("#########DEBUG##########")
        #print("mapping_path:")
        #print(mapping_path)
        energy, latency, cme = api.get_hardware_performance_zigzag(
            WORKLOAD_PATH,
            ACCELERATOR_PATH,
            mapping_path,
            opt="latency",
            dump_folder="BA_zigzag/zigzag_output/{datetime}.json",
            pickle_filename="BA_zigzag/zigzag_output/list_of_cmes.pickle"
        )
        print("################ DEBUG ##############")
        print("ZIGZAG EVALUATOR CALLED!")
        error_artifacts = {}
        return set_metric(1.0, energy, latency, error_artifacts)


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