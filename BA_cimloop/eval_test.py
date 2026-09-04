import os
import importlib.util
import traceback

from openevolve.evaluation_result import EvaluationResult

import accelforge as af
from accelforge.frontend.spec import Spec
from accelforge.model.main import evaluate_mapping, InvalidMappingError
from accelforge.util.parallel import set_n_parallel_jobs
#from _load_spec import get_spec

#/home/ansi/Documents/cimloop/accelforge/examples/arches/compute_in_memory/_load_spec.py

LOAD_SPEC_PATH = "/home/ansi/Documents/cimloop/accelforge/examples/arches/compute_in_memory/_load_spec.py"
_load_spec_module_spec = importlib.util.spec_from_file_location("get_spec", LOAD_SPEC_PATH)
_load_spec_module = importlib.util.module_from_spec(_load_spec_module_spec)
_load_spec_module_spec.loader.exec_module(_load_spec_module)
get_spec = _load_spec_module.get_spec

ARCH_NAME = "/home/ansi/Documents/openevolve/BA_cimloop/inputs/arch/basic_analog"          # Name ohne .yaml, wie von get_spec() erwartet
BATCH_SIZE = 1

set_n_parallel_jobs(1)
#python openevolve-run.py BA_cimloop/initial_program.py BA_cimloop/eval_test.py --config BA_cimloop/config.yaml --iterations 10

def build_spec() -> Spec:
    """Baut Arch + Workload (fix) OHNE Mapping. Wird pro Evaluation neu
    aufgerufen, damit kein Zustand zwischen Kandidaten geteilt wird."""
    spec = get_spec(ARCH_NAME, add_dummy_main_memory=True)

    workload_path = af.examples.workloads.compute_in_memory.resnet18  # eigenen Pfad einsetzen
    spec.workload = af.Workload.from_yaml(
        workload_path, top_key="workload", jinja_parse_data={"BATCH_SIZE": BATCH_SIZE}
    )
    spec.renames = af.Renames.from_yaml(
        workload_path, top_key="renames", jinja_parse_data={"BATCH_SIZE": BATCH_SIZE}
    )
    return spec


def make_error_result(error_type: str, error_message: str, tb: str, suggestion: str) -> EvaluationResult:
    return EvaluationResult(
        metrics={
            "energy": 0.0,
            "latency": 0.0,
            "combined_score": 0.0,
        },
        artifacts={
            "error_type": error_type,
            "error_message": error_message,
            "full_traceback": tb,
            "suggestion": suggestion,
        },
    )


def calculate_combined_score(energy: float, latency: float) -> float:
    edp = energy * latency
    if edp <= 0:
        return 0.0
    return 1.0 / edp


def evaluate_mapping_object(spec: Spec, mapping: "af.Mapping") -> EvaluationResult:
    """Nimmt ein bereits im Speicher vorliegendes Mapping-Objekt (vom
    evolvierten Programm erzeugt), prueft es und bewertet es."""
    try:
        spec.mapping = mapping
        result = evaluate_mapping(spec)

    except InvalidMappingError as e:
        return make_error_result(
            error_type=type(e).__name__,
            error_message=str(e),
            tb=traceback.format_exc(),
            suggestion=(
                "Das Mapping wurde erfolgreich geparst, verletzt aber eine "
                "physikalische Randbedingung (Speicherkapazitaet, raeumlicher "
                "Fanout, oder eine fehlende Loop mit tile_shape=1 fuer eine "
                "Rank-Variable). Siehe error_message fuer Details."
            ),
        )

    except Exception as e:
        return make_error_result(
            error_type=type(e).__name__,
            error_message=str(e),
            tb=traceback.format_exc(),
            suggestion=(
                "Unerwarteter Fehler beim Aufbau/Zuweisen des Mappings (z.B. "
                "falsches Schema, fehlende Pflichtfelder, falscher Typ). Keine "
                "physikalische Mapping-Ungueltigkeit im engeren Sinn."
            ),
        )

    energy = result.energy()
    latency = result.latency()
    return EvaluationResult(
        metrics={
            "energy": energy,
            "latency": latency,
            "combined_score": calculate_combined_score(energy, latency),
        },
        artifacts={},
    )



def evaluate(program_path: str) -> EvaluationResult:
    print("****************************************************")
    print("DEBUG: evaluate called")
    # 1. Evolviertes Programm laden
    try:
        module_spec = importlib.util.spec_from_file_location("program", program_path)
        module = importlib.util.module_from_spec(module_spec)
        module_spec.loader.exec_module(module)
    except Exception as e:
        print("DEBUG: 1.")
        return make_error_result(
            error_type=type(e).__name__,
            error_message=str(e),
            tb=traceback.format_exc(),
            suggestion="Fehler beim Laden/Ausfuehren des generierten Programms (Syntaxfehler o.ae.).",
        )

    # 2. Mapping-Objekt aus dem evolvierten Programm holen
    try:
        """
        spec = importlib.util.spec_from_file_location("program", program_path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        func = getattr(mod, "generate_mapping")
        """
        generate_mapping = getattr(module, "generate_mapping")
        mapping = generate_mapping()  # erwartet: af.Mapping-Objekt (oder kompatibles Dict)

        if isinstance(mapping, dict):
            mapping = af.Mapping.model_validate(mapping)
        if not isinstance(mapping, af.Mapping):
            raise TypeError(
                f"generate_mapping() muss ein af.Mapping-Objekt (oder dict) "
                f"zurueckgeben, bekam {type(mapping).__name__}"
            )

    except Exception as e:
        print("DEBUG: 2.")
        print(f"EXCEPTION TYPE: {type(e).__name__}")
        print(f"EXCEPTION MESSAGE: {e}")
        traceback.print_exc()

        return make_error_result(
            error_type=type(e).__name__,
            error_message=str(e),
            tb=traceback.format_exc(),
            suggestion="generate_mapping() konnte kein gueltiges Mapping-Objekt erzeugen.",
        )

    # 3. Feste Arch+Workload-Spec bauen
    try:
        spec = build_spec()
    except Exception as e:
        print("DEBUG: 3.")
        print(f"EXCEPTION TYPE: {type(e).__name__}")
        print(f"EXCEPTION MESSAGE: {e}")
        traceback.print_exc()

        return make_error_result(
            error_type=type(e).__name__,
            error_message=str(e),
            tb=traceback.format_exc(),
            suggestion="Fehler beim Aufbau der festen Architektur/Workload-Spec -- kein Problem des Kandidaten.",
        )

    # 4. Mapping pruefen und bewerten
    #return evaluate_mapping_object(spec, mapping)
    print("#####################00000000000###########################")
    spec.mapping = mapping
    result = evaluate_mapping(spec)
    energy = result.energy()
    latency = result.latency()
    print("################################################")
    print("DEBUG: evaluate_mapping() called")
    print(f"energy: {energy!r} ({type(energy).__name__})")
    print(f"latency: {latency!r} ({type(latency).__name__})")

    return EvaluationResult(
        metrics={
            "energy": float(energy),
            "latency": float(latency),
            "combined_score": calculate_combined_score(energy, latency),
        },
        artifacts={},
    )
