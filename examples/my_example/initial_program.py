import numpy as np
count = [0]

# EVOLVE-BLOCK-START
def sorting_algorithm(rl: list[int]): 
    for i in range(len(rl)):
        for k in range(len(rl)-1):
            compare_count(count)    #every time values get compared, call this function
            if (rl[k] > rl[k+1]):
                temp = rl[k]
                rl[k] = rl[k+1]
                rl[k+1] = temp
    return count[0]
# EVOLVE-BLOCK-END

def compare_count(count):
    count[0]+=1

if __name__ == "__main__":
    
    rng = np.random.default_rng()
    input_list = rng.integers(200, size=200)
    
    #compares = [0]
    #swaps = [0]

    compares = sorting_algorithm(input_list)

    #print(input_list)
    #print("\n")
    #print("compares: " + str(compares[0]))
    #print("swaps: " + str(swaps[0]))