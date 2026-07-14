"""
-zigzag evaluator einbinden
-nach welcher metrik optimieren ? 
"""


from zigzag import api  

workload = "/zigzag_inputs/models/ my_workload"
accelerator = "/zigzag_inputs/hardware/ my_accelerator"
mapping = "/zigzag_inputs/mappings/ my_mapping -> für mich interessant, die anderen beiden verändern sich nicht"

energy, latency, cme = api.get_hardware_performance_zigzag(
    workload,
    accelerator,
    mapping,
    opt="latency",
    dump_folder="outputs/{datetime}.json",
    pickle_filename="outputs/list_of_cmes.pickle"
)

#eval part für:
#syntax correct? hat 


#-----------------------------von claude erzeugt, testen------------------------------------

import importlib.util
import traceback
import yaml
from openevolve.evaluation_result import EvaluationResult
from zigzag.api import get_hardware_performance_zigzag

WORKLOAD_PATH = "inputs/workload/my_model.onnx"
ACCELERATOR_PATH = "inputs/hardware/my_accelerator.yaml"


def _load_mapping_path(program_path: str) -> str:
    # laedt das evolvierte Programm dynamisch und ruft dessen generate_mapping() auf
    spec = importlib.util.spec_from_file_location("evolved_program", program_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  # kann SyntaxError/ImportError/Exception werfen
    return module.generate_mapping()  # muss Pfad zur geschriebenen .yaml zurueckgeben



def _fail(error_type: str, msg: str) -> EvaluationResult:
    return EvaluationResult(
        metrics={"valid": 0.0, "combined_score": 0.0},
        artifacts={"error_type": error_type, "error_message": msg},
    )


def evaluate(mapping_path: str) -> EvaluationResult:
    try:
        energy, latency, cmes = get_hardware_performance_zigzag(
            workload=WORKLOAD_PATH,
            accelerator=ACCELERATOR_PATH,
            mapping=mapping_path,
            opt="latency",
        )

    except yaml.YAMLError as e:
        return _fail("yaml_syntax", f"Mapping-YAML is not parsable, syntax is wrong: {e}")

    except ValueError as e:
        return _fail("schema_validation", f"Mapping violates Schema: {e}")

    except AssertionError as e:
        msg = str(e)
        if "SpatialMapping" in msg:
            return _fail("no_valid_spatial_mapping", msg)
        if "mapping data" in msg:
            return _fail("layer_not_found", "Layer-Name in mapping doesn't match with workload")
        if not msg:
            return _fail("bad_file_extension", "filename has have .yaml ending")
        return _fail("assertion_error", msg)

    except KeyError as e:
        return _fail("unknown_key", f"referenced key does NOT exist: {e}")

    except IndexError as e:
        return _fail("malformed_list_entry", f"List has unexpected strcture/length: {e}")

    except Exception as e:
        # Catch-all für unbekannte/tiefere Pipeline-Fehler
        return _fail(type(e).__name__, f"{e}\n{traceback.format_exc()[-2000:]}")

    return EvaluationResult(
        metrics={
            "valid": 1.0,
            "energy": energy,
            "latency": latency,
            "combined_score": 1.0 / latency,
        },
        artifacts={},
    )
