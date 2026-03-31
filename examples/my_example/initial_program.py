# EVOLVE-BLOCK-START

import numpy as np

def sorting_algorithm(rl: list[int]) -> list[int]: 
    #compares | swaps
    metrics = [0,0]
    for i in range(len(rl)):
        for k in range(len(rl)-1):
            count_compares(metrics)
            if count_swaps(rl[k], rl[k+1], metrics):
                metrics[1]+=1
                temp = rl[k]
                rl[k] = rl[k+1]
                rl[k+1] = temp
    return metrics
# EVOLVE-BLOCK-END

def count_compares(metrics):
    metrics[0]+=1

def count_swaps(a: int, b:int, metrics):
    if(a > b):
        metrics[1]+=1;

if __name__ == "__main__":
    
    rng = np.random.default_rng()
    input_list = rng.integers(200, size=200)
    
    compares = [0]
    swaps = [0]

    sorting_algorithm(input_list)

    print(input_list)
    print("\n")
    print("compares: " + str(compares[0]))
    print("swaps: " + str(swaps[0]))