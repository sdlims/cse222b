import zlib
import binascii
import pprint
import sys
import random
import math
import matplotlib.pyplot as plt

prep_data = []
compression_result = {}

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

    #print("\n".join(prep_data))
    #breakpoint()

def get_subckt(indices):
    lineA = ""
    for i in indices:
        lineA += prep_data[i]+"\n"
    return lineA


def regularity_extraction(A, B):
    lineA = get_subckt(A)
    lineB = get_subckt(B)

    tplt_avg = (len(A) + len(B)) / 2

    size_penalty = 0
    template_penalty = 0

    # Punishes Having Different Sized Templates
    if len(A) > len(B):
        size_penalty = len(B) / (len(A) + len(B))
    elif (len(B) > len(A)):
        size_penalty = len(A) / (len(A) + len(B))
    else:
        size_penalty = 1
    
    # Punishes Based on Template Size
    if (tplt_avg <= 2) or (tplt_avg >= 10):
        template_penalty = 0.5
    elif (tplt_avg >= 3) and (tplt_avg <= 6):
        template_penalty = 1.3
    else:
        template_penalty = 1

 
    cmprA = zlib.compress(lineA.encode())
    cmprB = zlib.compress(lineB.encode())

    lineAB = lineA + lineB
    cmprAB = zlib.compress(lineAB.encode())

    return size_penalty * (len(cmprAB)/(len(cmprA) + len(cmprB))) 


# For some vector V, get the complete compression ratio
def compression_annealing(V):
    # print("Current V: ", V, "\n")
    subgraph = [[] for _ in range(max(V) + 1)]
    for i in range(len(V)):
        if (V[i]) == 0:
            continue
        else:
            subgraph[V[i]].append(i)

    # print(subgraph)

    compression_eq = 100
    for i in range(1, len(subgraph)):
        for j in range(i+1, len(subgraph)):
            if (len(subgraph[i]) == 0) or (len(subgraph[j]) == 0):
                continue
            else:
                compression_eq *= regularity_extraction(subgraph[i], subgraph[j])

    return (compression_eq / len(subgraph))
    
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

        if (current_cmpr > best_cmpr):
            best_V = current_V
            best_cmpr = current_cmpr
        

        temp *= cooling_rate
        iters += 1
    
    return (best_V, best_cmpr)
    # return best_cmpr

def simulated_change(V, cutoff):
    upp_b = len(V)
    low_b = 0

    # cutoff = 75

    idx = random.randint(0, upp_b - 1)
    change = random.randint(-1, 1)

    chance = random.randint(1, 100)

    copy_V = V[:]

    if (copy_V[idx] == upp_b):
        if (chance <= cutoff):
            # print("Swap!")
            intermediate = copy_V[idx]
            swap_idx = random.randint(0, upp_b - 1)
            copy_V[idx] = copy_V[swap_idx]
            copy_V[swap_idx] = intermediate
        else:
            # print("Change!")
            copy_V[idx] -= 1
    elif (copy_V[idx] == low_b):
        if (chance <= cutoff):
            # print("Swap!")
            intermediate = copy_V[idx]
            swap_idx = random.randint(0, upp_b - 1)
            copy_V[idx] = copy_V[swap_idx]
            copy_V[swap_idx] = intermediate
        else:
            # print("Change!")
            copy_V[idx] += 1
    else:
        if (chance <= cutoff):
            # print("Swap!")
            intermediate = copy_V[idx]
            swap_idx = random.randint(0, upp_b - 1)
            copy_V[idx] = copy_V[swap_idx]
            copy_V[swap_idx] = intermediate
        else:
            # print("Change!")
            copy_V[idx] += change

    return copy_V

def probability_calc(probability, trials, out_f):
    prob_result = [[] for _ in range(len(probability))]
    for i in range(len(probability)):
        for _ in range(trials):
            prob_result[i] += simulated_annealing([0, 0, 1, 1, 2, 3, 1, 1, 0, 4, 4, 4, 3, 2, 1, 2, 3, 3, 3, 2], 0.999, 10000, 1, 100000, probability[i])
        
        prob_result[i][1] = (prob_result[i][1]) / trials
    
    with open(out_f, "w") as file:
        count = 0
        for i in prob_result:
            file.write("Probability: " + str(probability[count]) + "\n" + "Compression: " + str(i[1]) + "\n" + "V: " + str(i[0]) + "\n\n")
            count += 1
    
    

def main():

    if (len(sys.argv) != 3):
        print(f"Usage: python3 {sys.argv[0]} <input_file> <output_file>")
        exit(1)
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    comparisons = []
    preprocess_data(input_file)

    probability = [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]
    trials = 1

    probability_calc(probability, trials, output_file)
    

    # print("Garbage:")
    # print(compression_annealing([0, 0, 1, 2, 2, 3, 1, 1, 1, 3, 2, 3, 2, 1, 0, 3, 2, 3, 2, 2]))
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



