import zlib
import binascii

regularity_dict = {}
block_size = 1

# # Obtain Instances from Netlist, then Generate Regularity
# def regularity_extraction(file_i):
#     line_num = 0
#     line_inter = ""
#     stall = 0
#     with open(file_i, "r") as file:
#         for line in file:
#             line_inter += line.strip() + " "
#             if ((line_inter.find(";") == -1) and (not line.isspace())):
#                 stall += 1
#             line_num = line_num + 1
#             if (line_inter.strip() == ""):
#                 continue
#             elif ((line_inter[-2] == ";")):
#                 parsed_set = token_parse(line_inter)
#                 # print(parsed_set)
#                 if (parsed_set[0] in regularity_dict):
#                     # print(line_num, stall)
#                     # print(line_inter)
#                     regularity_dict[parsed_set[0]].append(line_num - stall)
#                 else:
#                     regularity_dict[parsed_set[0]] = [line_num - stall]
#                 line_inter = ""
#                 stall = 0
#             else:
#                 continue

def regularity_extraction(file_i, A, B): # Assuming 0 as first line
    fp = open(file_i)
    lineA = ""
    lineB = ""
    A_busy = 0
    B_busy = 0
    if (A != B):
        for i, line in enumerate(fp):
            if (i == A) or (A_busy):
                lineA += line.strip() + " "
                if (lineA.find(";") != -1):
                    A_busy = 0
                    lineA = lineA.strip()
                    # print(lineA)
                else:
                    A_busy = 1
                    continue
            elif (i == B) or (B_busy):
                lineB += line.strip() + " "
                if (lineB.find(";") != -1):
                    B_busy = 0
                    lineB = lineB.strip()
                    # print(lineB)
                else:
                    B_busy = 1
                    continue
    cmprA = zlib.compress(lineA.encode('utf-8'), 2)
    cmprB = zlib.compress(lineB.encode('utf-8'), 2)

    cmprAB = zlib.compress(lineA.encode('utf-8') + lineB.encode('utf-8'), 2)

    return(len(cmprAB) / (len(cmprA) + len(cmprB)))



# Keeps track of everything: Instance, Instance Name, Content, and Line Count
def token_parse(str_i): # Operates assuming no comments
    token_dict = []
    str_i = str_i.strip()
    if (str_i.find(".") == -1):
        token_dict.append("N/A") # Not a Token
    else:
        if ((str_i[-2::] == ");")):
            #Instance
            first_whitespace = str_i.index(" ")
            token_dict.append(str_i[0:first_whitespace].strip())

            open_paran = str_i.index("(")

            #Instance Name
            token_dict.append(str_i[first_whitespace:open_paran].strip())

            #Content
            token_dict.append(str_i[open_paran:-1].strip())
    return token_dict

def main():
    # Identical
    print(regularity_extraction("/home/sdli/regularity_extraction/rtl/test.txt", 2, 3))
    
    #Complete Opposites
    print(regularity_extraction("/home/sdli/regularity_extraction/rtl/test.txt", 1, 8))
    
    #Somewhat Similar
    print(regularity_extraction("/home/sdli/regularity_extraction/rtl/test.txt", 1, 5))
    
    #Somewhat Similar Module Names, but NOT Regular
    print(regularity_extraction("/home/sdli/regularity_extraction/rtl/test.txt", 1, 14))
    # print(regularity_dict)

if __name__ == "__main__":
    main()



