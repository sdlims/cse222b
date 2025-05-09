import zlib
import binascii
import pprint
import sys
import random

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

    cmprA = zlib.compress(lineA.encode())
    cmprB = zlib.compress(lineB.encode())

    lineAB = lineA + lineB
    cmprAB = zlib.compress(lineAB.encode())

    return len(cmprAB)/(len(cmprA) + len(cmprB))


# For some vector V, get the complete compression ratio
def compression_annealing(V):
    subgraph = [[] for _ in range(max(V) + 1)]
    anti_onehot = len(subgraph) == len(prep_data)
    for i in range(len(V)):
        subgraph[V[i]].append(i)

    # print("Subgraphs: ", subgraph, "\n")

    compression_eq = 0
    for i in range(len(subgraph)):
        for j in range(len(subgraph)):
            if (i == j):
                continue
            else:
                # print("Comparison of\n", get_subckt(subgraph[i]), "\nand\n\n", get_subckt(subgraph[j]))
                # print("\nResult: ", regularity_extraction(subgraph[i], subgraph[j]), "\n")
                if (anti_onehot): # Or some other limitation to the compression
                    compression_eq += 0
                else:
                    compression_eq += regularity_extraction(subgraph[i], subgraph[j])

    return compression_eq
    
def compression_comparison(U, V):
    cmpr_U = compression_annealing(U)
    cmpr_V = compression_annealing(V)

    if (cmpr_U > cmpr_V):
        return U
    else:
        return V

def simulated_annealing(init_V, cooling_rate, start_temp, end_temp, max_iters): #end_temp might be redundant
    current_V = init_V
    current_cmpr = compression_annealing(init_V)

    best_V = current_V
    best_cmpr = current_cmpr

    temp = start_temp

    iters = 0
    while (temp > end_temp) and (iters < max_iters):
        neighbor_V = simulated_change(current_V)
        neighbor_cmpr = compression_annealing(current_V)

        # Unsure on Accepting Condition for Now
        if (random.randint(0, 1) == 1):
            current_V = neighbor_V
            current_cmpr = neighbor_cmpr

        if (current_cmpr > best_cmpr):
            best_V = current_V
            best_cmpr = current_cmpr
        

        temp *= cooling_rate
        iters += 1
    
    return (best_V, best_cmpr)

def simulated_change(V):
    idx = random.randint(0, len(V)-1)
    change = random.randint(-1, 1)

    copy_V = V[:]

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

    # print(compression_annealing([0, 0, 1, 1, 1, 2, 2, 0, 3, 1]))

    pprint.pprint(prep_data)

    print(simulated_annealing([0, 0, 1, 1, 2, 3, 1, 1, 0, 4, 4, 4, 3, 2, 1, 2, 3, 3, 3, 2], 0.99, 100, 1, 1000))


    # for i in range(len(prep_data)):
    #     for j in range(len(prep_data)):
    #         if i==j: 
    #             continue
    #         # Eventually these will be a list of indices, not just single instances
    #         A = [i]
    #         B = [j]
    #         regularity = regularity_extraction(A, B)
    #         comparisons.append((regularity,A,B))

    # sorted_comparisons = sorted(comparisons, key=lambda x: x[0])

    # with open(output_file, "w") as file:
    #     for i in range(100):
    #         regularity,A,B = sorted_comparisons[i]
    #         file.write(f"{i}\nComparison of :\n{get_subckt(A)} and\n{get_subckt(B)} {regularity}\n\n" )

    #pprint.pprint(sorted_comparisons)

if __name__ == "__main__":
    main()



