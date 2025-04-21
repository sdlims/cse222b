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


def indice_regularity_extraction(A, B): #A, B are lists with index pairs [start1, end1, start2, end2, ... ] Indexes prep_data which has instances
    lineA = ""
    lineB = ""

    a_i = 0
    a_j = 0
    while(a_i != len(A)):
        a_j = A[a_i]

        while(a_j != (A[a_i + 1] + 1)):
            lineA += prep_data[a_j - 1] + "\n"
            a_j += 1
        a_i += 2
    
    print("Final lineA: \n", lineA)

    b_i = 0
    b_j = 0
    while(b_i != len(B)):
        b_j = B[b_i]
        while(b_j != (B[b_i + 1] + 1)):
            lineB += prep_data[b_j - 1] + "\n"
            b_j += 1
        b_i += 2
    
    print("\nFinal lineB: \n", lineB)
    cmprA = zlib.compress(lineA.encode())
    cmprB = zlib.compress(lineB.encode())

    lineAB = lineA + lineB
    cmprAB = zlib.compress(lineAB.encode())

    return len(cmprAB)/(len(cmprA) + len(cmprB))

    


def main():
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    comparisons = []
    preprocess_data(input_file)
    regularity = indice_regularity_extraction([1, 2, 3, 5], [7, 9])

    comparisons.append((regularity,[1, 2, 3, 5], [7, 9]))

    print(comparisons)


    # if (len(sys.argv) != 3):
    #     print(f"Usage: python3 {sys.argv[0]} <input_file> <output_file>")
    #     exit(1)

    # input_file = sys.argv[1]
    # output_file = sys.argv[2]

    # comparisons = []
    # preprocess_data(input_file)

    # for i in range(9):
    #     for j in range(9):
    #         if (i == j):
    #             pass
    #         else:
    #             # Eventually these will be a list of indices, not just single instances
    #             A = [i]
    #             B = [j]
    #             regularity = regularity_extraction(A, B)
    #             comparisons.append((regularity,A,B))

    # sorted_comparisons = sorted(comparisons, key=lambda x: x[0])

    # with open(output_file, "w") as file:
    #     for i in range(10):
    #         regularity,A,B = sorted_comparisons[i]
    #         file.write(f"{i}\nComparison of :\n{get_subckt(A)} and\n{get_subckt(B)} {regularity}\n\n" )

    # pprint.pprint(compression_result)   

if __name__ == "__main__":
    main()



