import bz2
import pprint

prep_data = []
comp_data = []

scalar = 1.345

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
    comp.sort() # NEW LINE
    return comp


def nets_parse(data):
    start_idx = data.index("(")
    stop_idx = data.index(")")
    data = data[start_idx+1:stop_idx]
    data = data.split(",")
    data = [item.strip() for item in data]

    return data


def get_nets(indices):
    nets = []
    for i in indices:
        net_data = nets_parse(prep_data[i])

        max_len = max(net_data, key=len)
        norm_net_data = [item.zfill(len(max_len)) for item in net_data]
        nets.append(norm_net_data)
    
    return nets
    # print(nets)



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
            if (i == len(gateA)):
                re -= (1 / max(len(gateA), len(gateB)))
            elif (j == len(gateB)):
                re -= (1 / max(len(gateA), len(gateB)))
            elif (gateA[i] != gateB[j]):
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

    netA = get_nets(A)
    netB = get_nets(B)
    
    netAstr = ''.join(str(i) for i in netA)
    netBstr = ''.join(str(i) for i in netB)

    cmprAnet = bz2.compress(netAstr.encode())
    cmprBnet = bz2.compress(netBstr.encode())

    netABstr = netAstr + netBstr
    cmprABnet = bz2.compress(netABstr.encode())
    
    cmpr_gate = gate_re(gateA, gateB)

    cmprA = bz2.compress(lineA.encode())
    cmprB = bz2.compress(lineB.encode())

    lineAB = lineA + lineB
    cmprAB = bz2.compress(lineAB.encode())

    cmpr_main = (len(cmprAB) / (len(cmprA) + len(cmprB)))

    cmpr_net_main = (len(cmprABnet) / (len(cmprAnet) + len(cmprBnet)))


    return cmpr_main * cmpr_gate * cmpr_net_main * scalar # Scalar normalizes answers [0:1]