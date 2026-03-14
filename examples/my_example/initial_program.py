# EVOLVE-BLOCK-START

import numpy as np

def my_problem(rl):
    
    for i in range(len(rl)):
        for k in range(len(rl)-1):
            count_compares()
            if count_swaps(rl[k], rl[k+1]):
                temp = rl[k]
                rl[k] = rl[k+1]
                rl[k+1] = temp
# EVOLVE-BLOCK-END

def count_swaps(a: int, b:int):
        compares[0] += 1
    if(a > b):
        swaps[0]+=1;
    return a > b


if __name__ == "__main__":
    
    rng = np.random.default_rng()
    input_list = rng.integers(200, size=200)
    
    compares = [0]
    compares[0] = 0
    swaps = [0]
    swaps[0] = 0

    my_problem(input_list)

    print(input_list)
    print("\n")
    print("compares: " + str(compares[0]))
    print("swaps: " + str(swaps[0]))