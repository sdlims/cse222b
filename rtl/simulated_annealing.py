import random
import math

import cost_func as cf
import regularity_extraction as re

def simulated_annealing(init_V, cooling_rate, start_temp, end_temp, max_iters, cutoff):
    current_V = init_V
    current_cmpr = cf.cost_func(init_V)

    best_V = current_V
    best_cmpr = current_cmpr

    temp = start_temp

    iters = 0
    while (temp > end_temp) and (iters < max_iters):
        neighbor_V = simulated_change(current_V, cutoff)
        neighbor_cmpr = cf.cost_func(neighbor_V)

        delta_energy = neighbor_cmpr - current_cmpr
        if (delta_energy > 0) or (random.random() < math.exp(delta_energy / temp)):
            current_V = neighbor_V
            current_cmpr = neighbor_cmpr

        if (current_cmpr > best_cmpr):
            best_V = current_V
            best_cmpr = current_cmpr

        temp *= cooling_rate
        iters += 1
    
    return (best_V, best_cmpr)


def simulated_change(V, cutoff):
    upp_b = len(V)
    low_b = 0

    idx = random.randint(0, upp_b - 1)

    chance = random.randint(1, 100)
    if (chance % 2 == 0):
        change = -1
    else:
        change = 1

    copy_V = V[:]

    cutoff = cutoff * 100

    if (copy_V[idx] >= (upp_b//2)):
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


