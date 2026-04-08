"""
evaluator for my problem

EvaluationResult Class from OpenEvolve:
    has wrapper function 
"""

import numyp as np
import traceback
from openevolve.evaluation_result import EvaluationResult


#is this really needed? -> only if this functionality should be encapsulated
def load_program(program_path: str):
    spec = importlib.util.spec_from_file_location("program", program_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def evaluate(program_path: str) -> EvaluationResult:
    
    #structure
    metrics={
        "compare_score_small": 0.0,
        "compare_score_large": 0.0,
        "swap_score_small": 0.0,
        "swap_score_large": 0.0,
        "combined_score": 0.0,
        "error": "some kind of error",
    }

    error_artifacts = {
                "error_type": "",
                "error_message": "",
                "suggestion": ""
            }
    """

        EvaluationResult is Dict[str:float]
            

        ->no timeout

        -is code better:
        ->comapre with baseline_random
        #if better or equal:
        ->compare with other examples
    """

    
    """
    try this 1:
    LET:
        alle syntax tests wurden bestanden, kein runtime error, input und output format passen
        -> der generierte algorithmus kann listen annhemen und verarbeitet sie, ohne dass er abstürzt
    test_collection = generate_test_data()
    create copy of test_collection
    SEI: generierter algorithmus := ai_sort()
    CALL ai_sort() for each list in test_collection_cpy
    CALL is_sorted() for each list in test_collection_cpy
    """
    """
    try this 2:
    LET:
        ai_sort() is sorting everyting correctly
    CALL my_sort() for each test of test_collection -> baseline
    compare result of my_sort with result of ai_sort() -> create EvaluationResult
    """



    try:
        spec = importlib.util.spec_from_file_location("program", program_path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)

        try:
            #placeholder vlaues
            comp=0
            swap=0
            benchmark = [comp, swap]
            
            #has ai_search() correct return type?
            if (isinstance(benchmark, list) and len(benchmark) == 2):
                print("ai_sort() has correct output format")    
                #check if ai_sort() actually works -> check if sorted lists are sorted
            else:   
                error_artifacts = {
                "error_type": "Wrong return type",
                "error_message": "Return value is not the required type: [int, int]",
                "suggestion": "enforce usage of correct type"
                }

                return EvaluationResult(
                    metrics={
                        "compare_score_small": 0.0,
                        "compare_score_large": 0.0,
                        "swap_score_small": 0.0,
                        "swap_score_large": 0.0,
                        "combined_score": 0.0,
                        "error": "Wrong return type",
                    },
                    artifacts=error_artifacts
                )
        finally:  
            pass
        

        #initialize test-data:
        test_collection = generate_test_data()
        test_collection_cpy = test_collection
    
        #ai_sort() is a placeholder for the name of the generated algorithm
        ai_sort_results = []
        ai_sort_results.append(ai_sort())

        #at least on list isnt sorted
        for l in test_collection:
            if (is_sorted(test_collection[l]) == 0):
                return EvaluationResult(
                    metrics={
                        "compare_score_small": 0.0,
                        "compare_score_large": 0.0,
                        "swap_score_small": 0.0,
                        "swap_score_large": 0.0,
                        "combined_score": 0.0,
                        "error": "List not sorted",
                    },
                    artifacts=error_artifacts
                )






    except Exception as e:
        print(f"Evaluation failed at most basic step: {str(e)}")
        print(traceback.format_exec())
        
        error_artifacts = {
            "error_type": type(e).__name__,
            "error_message": str(e),
            "full_traceback": traceback.format_exc(),
            "suggestion": "Check for syntax errors in generated code."
        }

        return EvaluationResult(
            metrics={
                "compare_score_small": 0.0,
                "compare_score_large": 0.0,
                "swap_score_small": 0.0,
                "swap_score_large": 0.0,
                "combined_score": 0.0,
                "error": str(e),
            },
            artifacts=error_artifacts
        )



    #placeholder until later
    some_dict = {}
    some_error_artifacts = {}
    return EvaluationResult(some_dict, some_error_artifacts)


#------------------------------------helper function------------------------------
def generate_test_data() -> list:
    rng = np.random.default_rng()
    test_cases = []
    test_cases.append(rng.integers(100, size=100))
    test_cases.append(rng.integers(500, size=200))
    test_cases.append(rng.integers(1000, size=1000))
    test_cases.append(rng.integers(2000, size=2000))
    #test_cases.append(rng.integers(4000, size=4000))
    #test edge cases
    test_cases.append([1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]) 
    sorted_list = []
    for i in range(500):
        sorted_list.append(i)
    test_cases.append(sorted_list)
    print("generating done!\n")

    return test_cases


def is_sorted(validate_this):
    is_sorted = 1
    for i in (len(validate_this)-1):
        if(validate_this[i] > validate_this[i+1]):
            is_sorted = 0
    return is_sorted

#call this function for the generated code
def generate_results(test_collection: list) -> dict:
    """
    just concept, correct syntax later
    dict metrics = {}

    for l in test_collection:
        metrics.add(my_sort(l))
    """
    pass

#-----------------------------------algorithm core-------------------------------
def count_compares(metrics):
    metrics[0]+=1

def count_swaps(a: int, b:int, metrics):
    if(a > b):
        metrics[1]+=1;

#use this to get baseline metrics
def my_sort(rl: list[int]) -> list[int]: 
    #compares | swaps
    benchmark = [0,0]
    for i in range(len(rl)):
        for k in range(len(rl)-1):
            count_compares(benchmark)
            if count_swaps(rl[k], rl[k+1], benchmark):
                benchmark[1]+=1
                temp = rl[k]
                rl[k] = rl[k+1]
                rl[k+1] = temp
    return benchmark


