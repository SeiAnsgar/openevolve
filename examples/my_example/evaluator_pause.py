"""
EvaluationResult Class from OpenEvolve:
    has wrapper function 
"""
import importlib.util
import numpy as np
import traceback
from openevolve.evaluation_result import EvaluationResult


def evaluate(program_path: str) -> EvaluationResult:
    
    """
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
    
    #####################################TODO:###################################
    """


    try:
        spec = importlib.util.spec_from_file_location("program", program_path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)

        if not hasattr(mod, "sorting_algorithm"):
            error_artifacts = {
                "error_type": "MissingFunction",
                "error_message": "Program is missing required 'sorting_algorithm' function",
                "suggestion": "Make sure your program includes a function named 'sorting_algorithm'",
            }
            
            return EvaluationResult(
               metrics={
                    "compare_score_small": 0.0,
                    "compare_score_large": 0.0,
                    "swap_score_small": 0.0,
                    "swap_score_large": 0.0,
                    "combined_score": 0.0,
                    "error": "Function has wrong name!",
                },
                artifacts=error_artifacts
            )
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
    

        #initialize test-data:
        test_collection = generate_test_data()
        test_collection_cpy = test_collection[:]

        #generate baseline results
        my_sort_results = []
        for l in test_collection_cpy:
            my_sort_results.append(my_sort(l))

        #generate ai_sort() results
        #ai_sort() is a placeholder for the name of the generated algorithm
        ai_sort_results = []
        for l in test_collection:
            ai_sort_results.append(mod.sorting_algorithm(l)) #->ai_search() ~> mod.sorting_algorithm()

        #check if ai_sort() sorted correctly
        is_sorted=0
        for check_sorted in test_collection_cpy:
            sorted_amount = is_sorted(check_sorted)
        if is_sorted == 0:
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

        calculate_metric(my_sort_results, ai_sort_results)

    except Exception as e:
        print(f"Evaluation failed at most basic step: {str(e)}")
        print(traceback.format_exc())
        
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
    test_cases.append(rng.integers(200, size=200))
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
    for i in range((len(validate_this)-1)):
        if(validate_this[i] > validate_this[i+1]):
            is_sorted = 0
    return is_sorted

def calculate_metric(my_results, ai_results):
    #[comp_score, swap_score]
    compare_score_small=0.0
    compare_score_large=0.0
    swap_score_small=0.0
    swap_score_large=0.0
    compare_edge=0.0
    swap_edge=0.0
    combined=0.0

    compare_score_small = (my_results[0][0] + my_results[1][0])  - (ai_results[0][0] + ai_results[1][0])
    compare_score_large = (my_results[2][0] + my_results[3][0]) - (ai_results[2][0] + ai_results[3][0])
    swap_score_small = (my_results[0][1] + my_results[1][1]) - (ai_results[0][1] + ai_results[1][1])
    swap_score_large = (my_results[2][1] + my_results[3][1]) - (ai_results[2][1] + ai_results[3][1])
    
    compare_edge = (my_results[4][0] + my_results[5][0])  - (ai_results[4][0] + ai_results[5][0])
    swap_edge = (my_results[4][1] + my_results[5][1]) - (ai_results[4][1] + ai_results[5][1])
    combined = (compare_score_small + compare_score_large + swap_score_small + swap_score_large + compare_edge + swap_edge)/6


    return EvaluationResult(
            metrics={
                "compare_score_small": compare_score_small,
                "compare_score_large": compare_score_large,
                "swap_score_small": swap_score_small,
                "swap_score_large": swap_score_large,
                "combined_score": combined,
                "error": "no error found",
            },
            artifacts=error_artifacts
        )

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


