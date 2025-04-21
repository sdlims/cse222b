import zlib
import binascii
import pprint

in_f = "/home/sdli/regularity_extraction/rtl/test.txt"
reg_f = "/home/sdli/regularity_extraction/regularity/aes.gate.v"
out_f = "/home/sdli/regularity_extraction/rtl/test_o.txt"

prep_data = {}
compression_result = {}

def preprocess_data(file_i):
    global line_cnt
    line_cnt = 0
    with open(file_i, "r") as file:
        for line in file:
            prep_data[line_cnt] = line
            line_cnt += 1
    
    # print(prep_data)


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
    # preprocess_data(in_f)
    preprocess_data(reg_f)
    with open(out_f, "w") as file:
        for i in range(17225, 17725):
            for j in range(17225, 17725):
                if (i == j):
                    pass
                else:
                    regularity, outA, outB = (block_regularity_extraction(i, i, j, j))
                    if (regularity <= 0.7): # Identical features are usually between this range, but may need to adjust later
                        if (outA != ");") and (outB != ");") and (outA.strip() != "") and (outB.strip() != ""):
                            compression_result[str(i+1) + ", " + str(i+1) + ", " + str(j+1) + ", " + str(j+1)] = regularity
                            file.write("Comparison of " + outA + "  and  " + outB + ":  " + str(regularity) + "\n" + "\n")

    # pprint.pprint(compression_result)   

if __name__ == "__main__":
    main()



