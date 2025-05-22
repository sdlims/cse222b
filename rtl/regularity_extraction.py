import bz2

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


def size_re(lenA, lenB):
    if (lenA != lenB):
        if (lenA > lenB):
            return (lenB / lenA)
        else:
            return (lenA / lenB)
    else:
        return 1

def gate_re(gateA, gateB):
    if (gateA == gateB):
        return 1
    else:
        re = 1.00
        i = 0
        j = 0
        while not ((i >= len(gateA)) and (j >= len(gateB))):
            if (gateA[i] != gateB[j]):
                re -= (1 / max(len(gateA), len(gateB)))
            if (i != len(gateA)):
                i += 1
            if (j != len(gateB)):
                j += 1
        return re

def regularity_extraction(A, B):
    lineA = get_subckt(A)
    lineB = get_subckt(B)

    gateA = get_subgate(A)
    gateB = get_subgate(B)

    cmpr_gate = gate_re(gateA, gateB)

    cmprA = bz2.compress(lineA.encode())
    cmprB = bz2.compress(lineB.encode())

    lineAB = lineA + lineB
    cmprAB = bz2.compress(lineAB.encode())

    cmpr_main = (len(cmprAB) / (len(cmprA) + len(cmprB)))

    cmpr_size = size_re(len(A), len(B))

    return cmpr_main * cmpr_size * cmpr_gate