import zlib
import binascii
import pprint
import sys

prep_data = []
compression_result = {}

def preprocess_data(file_i):
    global line_cnt
    line_cnt = 0
    
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

def block_regularity_extraction(A_s, A_e, B_s, B_e):
    lineA = ""
    lineB = ""
    busy = 0
    while (A_s <= A_e) or (busy):
        lineA += prep_data[A_s].strip()
        if (A_s >= A_e) and (not lineA.endswith(";")):
            busy = 1
        elif (lineA.endswith(";")):
            busy = 0
        if (A_s == line_cnt - 1):
            break
        else:
            A_s += 1
    
    
    while (B_s <= B_e) or (busy): 
        lineB += prep_data[B_s].strip()
        if (B_s >= B_e) and (not lineB.endswith(";")):
            busy = 1
        elif (lineB.endswith(";")):
            busy = 0
        if (B_s == line_cnt - 1):
            break
        else:
            B_s += 1
    
    cmprA = zlib.compress(lineA.encode())
    cmprB = zlib.compress(lineB.encode())

    lineAB = lineA + lineB
    cmprAB = zlib.compress(lineAB.encode())

    return(len(cmprAB)/(len(cmprA) + len(cmprB)), lineA, lineB)


def main():
    if (len(sys.argv) != 3):
        print(f"Usage: python3 {sys.argv[0]} <input_file> <output_file>")
        exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    comparisons = []
    preprocess_data(input_file)

    for i in range(10):
        for j in range(10):
            if (i == j):
                pass
            else:
                # Eventually these will be a list of indices, not just single instances
                A = [i]
                B = [j]
                regularity = regularity_extraction(A, B)
                comparisons.append((regularity,A,B))

    sorted_comparisons = sorted(comparisons, key=lambda x: x[0])

    with open(output_file, "w") as file:
        for i in range(10):
            regularity,A,B = sorted_comparisons[i]
            file.write(f"{i}\nComparison of :\n{get_subckt(A)} and\n{get_subckt(B)} {regularity}\n\n" )

    # pprint.pprint(compression_result)   

if __name__ == "__main__":
    main()



