"""
evaluator for my problem

general evaluator structure:


import <..>

def timeout_handling (optional? -> can be run with or without timeout condition)

def evaluate(program_path: str)
    bekanntes optimum als baseline nehmen

    try:
        load problem
"""

import numyp as np
from openevolve.evaluation_result import EvaluationResult

def load_program(program_path):
    spec = importlib.util.spec_from_file_location("program", program_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def evaluate(program_path: str) -> EvaluationResult:
    """
        evaluate..
        - run programm with test_case[]
            -> catch errors and execptions
        - check for runtim -> after certain time, call timeout
    """


    compares = [0]
    compares[0] = 0
    swaps = [0]
    swaps[0] = 0

    def count_swaps(a: int, b:int):
        compares[0] += 1
    if(a > b):
        swaps[0]+=1;
    return a > b


    return {"Swaps: ":swaps[0],
            "compares:" compares[0]
        

    }

def generate_test_data():

    test_cases = [random_list_p2, random_list_p3, random_list_p4, random_list_p5, random_list_p6, equal_list, sorted_list]
    rng = np.random.default_rng()
    random_list_p2 = rng.integers(100, size=100)
    random_list_p3 = rng.integer(1000, size=1000)
    random_list_p4 = rng.integer(10000, size=10000)
    random_list_p5 = rng.integer(100000, size=100000)
    random_list_p6 = rng.integer(1000000, size=1000000)

    #test edge cases
    equal_list = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
    for i in range(1000):
        sorted_list = i
    
def generate_baseline_results():
    #fill dictionary -> test_case_x{(comps,swaps)}


def my_problem(rl):    
    for i in range(len(rl)):
        for k in range(len(rl)-1):
            count_compares()
            if count_swaps(rl[k], rl[k+1]):
                temp = rl[k]
                rl[k] = rl[k+1]
                rl[k+1] = temp