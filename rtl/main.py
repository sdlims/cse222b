import zlib
import binascii
import pprint
import sys

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
def compression_anealling(V):
    subgraph = [[] for _ in range(max(V) + 1)]
    for i in range(len(V)):
        subgraph[V[i]].append(i)
    
    # return(subgraph)

    compression_eq = 0
    for i in range(len(subgraph)):
        for j in range(len(subgraph)):
            if (i == j):
                continue
            else:
                # print("Comparison of\n", get_subckt(subgraph[i]), "\nand\n\n", get_subckt(subgraph[j]))
                # print("\nResult: ", regularity_extraction(subgraph[i], subgraph[j]), "\n")
                compression_eq += regularity_extraction(subgraph[i], subgraph[j])

    return compression_eq
    


def main():

    if (len(sys.argv) != 3):
        print(f"Usage: python3 {sys.argv[0]} <input_file> <output_file>")
        exit(1)
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    comparisons = []
    preprocess_data(input_file)

    print(compression_anealling([0, 0, 1, 1, 1, 2, 2, 0, 3, 1]))

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



