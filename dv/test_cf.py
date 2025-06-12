# clear && python3 rtl/test_cf.py regularity/pseudo_adder.txt

import sys
import random
import pprint
import numpy as np
import matplotlib.pyplot as plt

sys.path.append(r'/home/sdli/regularity_extraction/rtl/')

import regularity_extraction as re
import cost_func as cf

# For Ripple:
def solutions(input_file):
    match (input_file):
        case "regularity/pseudo_adder.txt":
            opt_sol         = [1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4]
            # adjacent_sol    = [1, 1, 2, 2, 2, 3, 3, 4, 4, 4, 5, 5, 6, 6, 6, 7, 7, 8, 8, 8]
            # one_step_right  = [1, 1, 1, 1, 2, 2, 2, 2, 2, 1, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4]
            # one_step_left   = [1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4]
            # bad_sol         = [1, 1, 2, 2, 3, 3, 3, 3, 4, 5, 6, 6, 7, 7, 6, 6, 1, 1, 2, 3]

    # For 4x4 Mult:
        case "regularity/pseudo_4x4_mult.txt":
            opt_sol                     = [1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 0, 5, 5, 6, 6, 6, 6, 6, 7, 7, 7, 7, 7, 8, 8, 9, 9, 10, 10, 10, 10, 10, 11, 11, 11, 11, 11, 12, 12, 12, 12, 12, 13, 13, 14, 14, 15, 15, 15, 15, 15, 16, 16, 16, 16, 16, 17, 17, 17, 17, 17, 0, 0, 0, 0, 0]
            # adjacent_sol                = [1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 0, 5, 5, 6, 6, 6, 25, 25, 7, 7, 7, 24, 24, 8, 8, 9, 9, 10, 10, 10, 23, 23, 11, 11, 11, 22, 22, 12, 12, 12, 21, 21, 13, 13, 14, 14, 15, 15, 15, 20, 20, 16, 16, 16, 19, 19, 17, 17, 17, 18, 18, 0, 0, 0, 0, 0]
            # one_step_right              = [1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 0, 5, 5, 6, 6, 6, 6, 6, 7, 7, 7, 7, 7, 8, 8, 9, 9, 10, 10, 10, 10, 10, 11, 11, 11, 11, 11, 12, 12, 12, 12, 12, 13, 13, 14, 14, 15, 15, 15, 15, 15, 16, 16, 16, 16, 17, 17, 17, 17, 17, 16, 0, 0, 0, 0, 0]
            # one_step_left               = [1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 0, 5, 5, 6, 6, 6, 6, 6, 7, 7, 7, 7, 7, 8, 8, 9, 9, 10, 10, 10, 10, 10, 11, 11, 11, 11, 11, 12, 12, 12, 12, 12, 13, 13, 14, 14, 15, 15, 15, 15, 15, 16, 16, 16, 16, 17, 17, 17, 17, 17, 17, 0, 0, 0, 0, 0]
            # bad_sol                     = [1, 1, 2, 2, 3, 3, 3, 3, 4, 5, 6, 6, 7, 7, 6, 6, 1, 1, 2, 3, 1, 1, 2, 2, 3, 3, 3, 3, 4, 5, 6, 6, 7, 7, 6, 6, 1, 1, 2, 3, 1, 1, 2, 2, 3, 3, 3, 3, 4, 5, 6, 6, 7, 7, 6, 6, 1, 1, 2, 3, 1, 1, 2, 2, 3, 3, 3, 3, 4, 5, 6, 6]
        case "regularity/unit_test_1.txt":
            opt_sol = [1, 1, 1, 2, 2, 2]
        case "regularity/unit_test_2.txt":
            opt_sol = [1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0]
        case "regularity/unit_test_3.txt":
            opt_sol = [1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3]
    return opt_sol

def simulated_change(V):
    cutoff = 65

    upp_b = len(V)
    low_b = 0

    idx = random.randint(0, upp_b - 1)

    chance = random.randint(1, 100)
    change = random.choice([-1, 1])

    copy_V = V[:]

    if (copy_V[idx] >= (upp_b)):
        if (chance <= cutoff):
            swap_idx = random.randint(0, len(V) - 1)
            copy_V[idx], copy_V[swap_idx] = copy_V[swap_idx], copy_V[idx]

        else:
            copy_V[idx] -= 1

    elif (copy_V[idx] == low_b):
        if (chance <= cutoff):
            swap_idx = random.randint(0, len(V) - 1)
            copy_V[idx], copy_V[swap_idx] = copy_V[swap_idx], copy_V[idx]

        else:
            copy_V[idx] += 1

    else:
        if (chance <= cutoff):
            swap_idx = random.randint(0, len(V) - 1)
            copy_V[idx], copy_V[swap_idx] = copy_V[swap_idx], copy_V[idx]

        else:
            copy_V[idx] += change

    return copy_V

def make_changes(init_V, iters):
    changes = []
    opt_cost = round(cf.cost_func(init_V), 2)
    changes.append(opt_cost)
    current_sol = init_V
    
    while (iters != 0):
        neighbor_sol = simulated_change(current_sol)
        neighbor_cost = round(cf.cost_func(neighbor_sol), 2)
        if (neighbor_cost < opt_cost):
            print("Wuh oh!")
            print(neighbor_sol)
        changes.append(neighbor_cost)
        current_sol = neighbor_sol
        iters -= 1
    
    return np.array(changes)


def main():
    changes = []
    input_file = sys.argv[1]
    re.preprocess_data(input_file)
    opt_sol = solutions(input_file)

    
    it_st = 12
    x = np.arange(0, it_st+1)

    trials = 100
    changes_out = [[] for _ in range(trials)]
    y = []
    for i in range(trials):
        changes_out[i] = np.array(make_changes(opt_sol, it_st))
        # print(changes_out)
    
    out = 0
    for i in range(trials):
        out += changes_out[i]
    
    y = out / trials

    plt.xticks(x)
    plt.yticks(y)

    plt.xlabel("Steps from Optimal")
    plt.ylabel("Cost of V")
    plt.title("Comparison of Cost Func Across Iterative Changes (Unit Test 3)")
    
    plt.plot(x, y, color='blue', marker='o', linestyle='-', markerfacecolor='red', markeredgecolor='red')
    plt.show()


if __name__ == "__main__":
    main()