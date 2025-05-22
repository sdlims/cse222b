import zlib
import bz2
import binascii
import pprint
import sys
import random
import math
import matplotlib.pyplot as plt


prep_data = []
comp_data = []

def preprocess_data(file_i):
    init_data = []
    init_data.append("")
    with open(file_i, "r") as file:
        for line in file:
            line = line.strip()
            init_data[-1] += line
            if line.endswith(";"):
                init_data.append("")
    
    for line in init_data:
        if line.startswith("//"):
            continue
        if line.startswith("module"):
            continue
        if line.startswith("endmodule"):
            continue
        if line.startswith("input"):
            continue
        if line.startswith("output"):
            continue
        if line.startswith("wire"):
            continue
        # Skip these non-functional cells
        if "FILLER" in line:
            continue
        if "TAPCELL" in line:
            continue
        if "DECAP" in line:
            continue
        prep_data.append(line)

        idx = line.find(" ")
        comp_data.append(line[0:idx])

    #print("\n".join(prep_data))
    #breakpoint()

def get_subckt(indices):
    lineA = ""
    for i in indices:
        lineA += prep_data[i]
    return lineA

def get_subgate(indices):
    comp = []
    for i in range(len(indices)):
        comp.append(comp_data[indices[i]])
    return comp

def regularity_extraction(A, B):
    lineA = get_subckt(A)
    lineB = get_subckt(B)

    gateA = get_subgate(A)
    gateB = get_subgate(B)

    if (gateA == gateB):
        template_identicality = 1.1
    else:
        template_identicality = 0.9

    # Punishes Having Different Sized Templates
    if len(A) > len(B):
        size_adjust = (len(B)) / (len(A))
    elif (len(B) > len(A)):
        size_adjust = (len(A)) / (len(B))
    else:
        size_adjust = 1.5

    lineAB = lineA + lineB
    cmprAB = bz2.compress(lineAB.encode())

    cmpr_out = len(lineAB) / len(cmprAB)

    # print("Compression Ratio: ", cmpr_out)
    # print("Size Adjustments: ", size_adjust)
    # print("Template Average Size: ", tplt_avg, "\n")

    return (size_adjust * cmpr_out * template_identicality) 


# For some vector V, get the complete compression ratio
def compression_annealing(V):
    # print("Current V: ", V, "\n")
    subgraph = [[] for _ in range(max(V) + 1)]
    for i in range(len(V)):
        if (V[i]) == 0:
            continue
        else:
            subgraph[V[i]].append(i)

    # print("Subgraph: ", subgraph)

    compression_eq = 0
    cmpr_cnt = 0
    for i in range(1, len(subgraph)):
        for j in range(i+1, len(subgraph)):
            cmpr_cnt += 1
            if (len(subgraph[i]) == 0) or (len(subgraph[j]) == 0):
                continue
            else:
                # print("Comparing ", subgraph[i], "and", subgraph[j])
                compression_eq += regularity_extraction(subgraph[i], subgraph[j])
                # print("Compression Out: ", compression_eq, "\n")

    # print("Compression Out: ", compression_eq)
    # print("# of Subgraphs: ", len(subgraph) - 1, "\n")
    return (compression_eq / cmpr_cnt) if cmpr_cnt else 0 #Averages
    
def compression_comparison(U, V):
    cmpr_U = compression_annealing(U)
    cmpr_V = compression_annealing(V)

    if (cmpr_U > cmpr_V):
        return U
    else:
        return V

def simulated_annealing(init_V, cooling_rate, start_temp, end_temp, max_iters, cutoff): #end_temp might be redundant
    current_V = init_V
    current_cmpr = compression_annealing(init_V)

    best_V = current_V
    best_cmpr = current_cmpr

    temp = start_temp

    iters = 0
    while (temp > end_temp) and (iters < max_iters):
        neighbor_V = simulated_change(current_V, cutoff)
        neighbor_cmpr = compression_annealing(neighbor_V)

        delta_energy = neighbor_cmpr - current_cmpr
        if (delta_energy > 0) or (random.random() < math.exp(delta_energy / temp)):
            current_V = neighbor_V
            current_cmpr = neighbor_cmpr

            # print("Current V: ", current_V)
            # print("Current Cmpr: ", current_cmpr)

        if (current_cmpr > best_cmpr):
            best_V = current_V
            best_cmpr = current_cmpr

            # print("\nNew Best V: ", best_V)
            # print("New Best Cmpr: ", best_cmpr)

            # print("Updating Best V\n")
        

        temp *= cooling_rate
        iters += 1
    
    return (best_V, best_cmpr)
    # return best_cmpr


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
            # print("Swap!")
            swap_idx = random.randint(0, len(V) - 1)
            copy_V[idx], copy_V[swap_idx] = copy_V[swap_idx], copy_V[idx]

        else:
            # print("Change!")
            copy_V[idx] -= 1

    elif (copy_V[idx] == low_b):
        if (chance <= cutoff):
            # print("Swap!")
            swap_idx = random.randint(0, len(V) - 1)
            copy_V[idx], copy_V[swap_idx] = copy_V[swap_idx], copy_V[idx]

        else:
            # print("Change!")
            copy_V[idx] += 1

    else:
        if (chance <= cutoff):
            # print("Swap!")
            swap_idx = random.randint(0, len(V) - 1)
            copy_V[idx], copy_V[swap_idx] = copy_V[swap_idx], copy_V[idx]

        else:
            # print("Change!")
            copy_V[idx] += change

    return copy_V



def main():

    if (len(sys.argv) != 3):
        print(f"Usage: python3 {sys.argv[0]} <input_file> <output_file>")
        exit(1)
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    comparisons = []
    preprocess_data(input_file)

    #[1, 1, 1, 1, 1, 2, 2, 2, 2, 4, 3, 3, 3, 3, 3, 4, 4, 4, 4, 2]
    init_V = [random.randint(0, len(prep_data)//4) for _ in range(len(prep_data))]
    random.shuffle(init_V)
    pprint.pprint(simulated_annealing([1, 1, 1, 2, 2, 2, 3, 3, 4, 4, 4, 4, 5, 5, 5, 1, 1, 1, 1, 2], 0.98, 10, 0.01, 5000, 0.8))
    

    # print("Garbage:")
    # print(compression_annealing([1, 1, 1, 1, 1, 2, 2, 2, 2, 4, 3, 3, 3, 3, 3, 4, 4, 4, 4, 2]))
    # print("\n")

    # print("Garbage:")
    # print(compression_annealing([1, 2, 3, 1, 4, 3, 4, 4, 3, 4, 1, 2, 2, 1, 3, 3, 2, 2, 1, 4]))
    # print("\n")

    # print("Garbage:")
    # print(compression_annealing([3, 3, 3, 3, 2, 4, 3, 1, 4, 4, 2, 2, 2, 2, 1, 1, 4, 4, 1, 1]))
    # print("\n")
    

    # print("Group each Ripple Adder:")
    # print(compression_annealing([1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4]))
    # print("\n")

    # print("Group By Output:")
    # print(compression_annealing([1, 1, 2, 2, 2, 3, 3, 4, 4, 4, 5, 5, 6, 6, 6, 7, 7, 8, 8, 8]))


    # print("Group each Ripple Adder:")
    # print(simulated_annealing([1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4], 0.99, 10000, 1, 10000, 0.8))
    # print("\n")
    # print("Group By Output:")
    # print(simulated_annealing([1, 1, 2, 2, 2, 3, 3, 4, 4, 4, 5, 5, 6, 6, 6, 7, 7, 8, 8, 8], 0.99, 10000, 1, 10000, 0.8))


if __name__ == "__main__":
    main()