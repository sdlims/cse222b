import zlib
import binascii
import token
import tokenize
import io

regularity_dict = {}

# Obtain Instances from Netlist, then Generate Regularity
    # Does NOT work for multi-line instances
def regularity_extraction(file_i):
    parsed_set = []
    line_num = 0;
    with open(file_i, "r") as file:
        for line in file:
            line_num = line_num + 1
            # print(line.rstrip())
            parsed_set = token_parse(str(line), 0)
            if (parsed_set[0] in regularity_dict):
                regularity_dict[parsed_set[0]].append(line_num)
            else:
                regularity_dict[parsed_set[0]] = [line_num]
    
    print(regularity_dict)


# Keeps track of everything: Instance, Parameters, Instance Name, Content, and Line Count
def token_parse(str_i, line_num_i): # Operates assuming no comments
    token_dict = []
    str_i = str_i.rstrip()
    if (str_i[-2::] == ");"):
        if (str_i.find("#") != -1): # Parameter Checking
            #Instance
            first_whitespace = str_i.index(" ")
            token_dict.append(str_i[0:first_whitespace])

            #Parameters
            first_open_paran   = str_i.index("(")
            first_closed_paran = str_i.index(")")
            token_dict.append(str_i[first_open_paran-1:first_closed_paran+1].strip())

            second_closed_paran = str_i.index(")", first_closed_paran+1)
            last_open_paran   = str_i.index("(", first_closed_paran+1)

            #Instance Name
            token_dict.append(str_i[first_closed_paran+1:last_open_paran].strip())

            #Content
            token_dict.append(str_i[last_open_paran:-1].strip())

        else:                       # No Parameter
            #Instance
            first_whitespace = str_i.index(" ")
            token_dict.append(str_i[0:first_whitespace].strip())

            open_paran = str_i.index("(")

            #Parameters
            token_dict.append("N/A")

            #Instance Name
            token_dict.append(str_i[first_whitespace:open_paran].strip())

            #Content
            token_dict.append(str_i[open_paran:-1].strip())
    return token_dict


regularity_extraction("/home/sdli/regularity_extraction/rtl/test.txt")



