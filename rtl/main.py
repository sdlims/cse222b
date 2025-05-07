# clear && python3 rtl/main.py rtl/test.txt rtl/test_o.txt
# clear && python3 rtl/main.py regularity/aes.gate.v rtl/test_o.txt

import zlib
import binascii
import pprint
import sys

prep_data = []

inst_i = ['A', 'A1', 'A2', 'B']
inst_o = ['Y']

ckt_input = {'Global': []}
ckt_output = {'Global': []}

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
            if(line.find("[") == -1):
                # if not (ckt_input.get("Global")):
                #     ckt_input["Global"] = list(line[6:-1])
                # else:
                #     ckt_input["Global"].append(line[6:-1])
                ckt_input['Global'].append(line[6:-1])
            else:
                ind = line.index("]")
                ckt_input['Global'].append(line[ind+2:-1])
            continue
        if line.startswith("output"):
            if(line.find("[") == -1):
                ckt_output['Global'].append(line[7:-1])
            else:
                ind = line.index("]")
                ckt_output['Global'].append(line[ind+2:-1])
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


def get_port_io(port_i):
    return 0


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


def conn_map(str_i): #Doesn't work if run on entire netlist, only should be run on instances, NOT wires
    
    if (str_i.startswith("wire")):
        return (0, 0)
    pin_o =  []
    conn_o = []
    start_ind = str_i.index("(") # Starting Index is first instance of (
    str_temp = ""
    for i in range(start_ind, len(str_i)):
        if (str_i[i] == "."):
            j = i
            while(str_i[j] != "(") and (str_i[j] != ")"):
                str_temp += str_i[j]
                j += 1
            pin_o.append(str_temp[1::])
            str_temp = ""
        elif (str_i[i] == "(") and (i != start_ind):
            j = i
            while(str_i[j] != ")"):
                str_temp += str_i[j]
                j += 1
            conn_o.append(str_temp[1::])
            str_temp = ""
    
    return(pin_o, conn_o)
            



# -------------------------------------------------------------------------------- #



def main():
    if (len(sys.argv) != 3):
        print(f"Usage: python3 {sys.argv[0]} <input_file> <output_file>")
        exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    preprocess_data(input_file)

    # Printing
    print("Inputs: ")
    pprint.pprint(ckt_input)

    print("Outputs: ")
    pprint.pprint(ckt_output)

    print("\n\n")

    for i in range(len(prep_data)):
        print(conn_map(prep_data[i]))

    # with open(output_file, "w") as file:
    #     for i in range(10):
    #         regularity,A,B = sorted_comparisons[i]
    #         file.write(f"{i}\nComparison of :\n{get_subckt(A)} and\n{get_subckt(B)} {regularity}\n\n" )

if __name__ == "__main__":
    main()



