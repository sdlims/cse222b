import zlib
import binascii

test_path = "/home/sdli/regularity_extraction/rtl/test.txt"
out_f = "/home/sdli/regularity_extraction/rtl/AB_compress.txt"

prep_data = {}

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
        if (A_s >= A_e) and (lineA[-1] != ";"):
            busy = 1
        else:
            busy = 0
        A_s += 1
    
    
    while (B_s <= B_e) or (busy): 
        lineB += prep_data[B_s].strip()
        if (B_s >= B_e) and (lineB[-1] != ";"):
            busy = 1
        else:
            busy = 0
        B_s += 1
    
    cmprA = zlib.compress(lineA.encode())
    cmprB = zlib.compress(lineB.encode())

    lineAB = lineA + lineB
    cmprAB = zlib.compress(lineAB.encode())

    return(len(cmprAB)/(len(cmprA) + len(cmprB)))


def main():
    # Identical
    # print(regularity_extraction("/home/sdli/regularity_extraction/rtl/test.txt", 2, 3))
    
    # #Complete Opposites
    # print(regularity_extraction("/home/sdli/regularity_extraction/rtl/test.txt", 1, 19))
    
    # #Somewhat Similar
    # print(regularity_extraction("/home/sdli/regularity_extraction/rtl/test.txt", 1, 5))
    
    # #Somewhat Similar Module Names, but NOT Regular
    # print(regularity_extraction("/home/sdli/regularity_extraction/rtl/test.txt", 1, 14))
    
    # print(regularity_extraction("/home/sdli/regularity_extraction/rtl/test.txt", 21, 22))

    # block_regularity_extraction(test_path, 2, 4, 5, 7)
    preprocess_data(test_path)
    with open(out_f, "w") as file:
        for i in range(line_cnt-2):
            for j in range(line_cnt-3):
                if (j == 0):
                    continue
                regularity = (block_regularity_extraction(i, i+1, j, j+1))
                file.write("Comparison of " + prep_data[i].strip() + "  and  " + prep_data[j].strip() + ":  " + str(regularity) + "\n" + "\n")


if __name__ == "__main__":
    main()



