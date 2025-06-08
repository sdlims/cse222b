# clear && python3 rtl/test_re.py regularity/pseudo_adder.txt

import sys
import random

sys.path.append(r'/home/sdli/regularity_extraction/rtl/')

import regularity_extraction as re

def main():
    input_file = sys.argv[1]
    re.preprocess_data(input_file)
    match input_file:
        case "regularity/unit_test_1.txt":
            print("Regularity on Itself                     : ", re.regularity_extraction([0, 1, 2], [0, 1, 2]))
            print("===========================================================================================")
            print("Regularity on Similar Template           : ", re.regularity_extraction([0, 1, 2], [3, 4, 5]))
            print("===========================================================================================")
            print("Regularity on Partial Template           : ", re.regularity_extraction([0, 1, 2], [2, 3, 4]))
            print("===========================================================================================")
            print("Regularity on Dissimilar Template        : ", re.regularity_extraction([0, 3, 4], [1, 2, 5]))


        case "regularity/unit_test_2.txt":
            print("Regularity on Itself                     : ", re.regularity_extraction([0, 1, 2, 3, 4], [0, 1, 2, 3, 4]))
            print("===========================================================================================")
            print("Regularity on Similar Template           : ", re.regularity_extraction([0, 1, 2, 3, 4], [5, 6, 7, 8, 9]))
            print("===========================================================================================")
            print("Regularity on Partial Template           : ", re.regularity_extraction([0, 1, 2, 3, 4], [10, 11, 12, 13, 14]))
            print("===========================================================================================")
            x = [random.randint(0, len(re.prep_data) - 1) for _ in range(5)]
            print("Regularity against ", x ,"   : ", re.regularity_extraction([0, 1, 2, 3, 4], x))
            print("===========================================================================================")
            print("Regularity on Dissimilar Template        : ", re.regularity_extraction([0, 1, 2, 3, 4], [6, 7, 8, 9, 10]))


        case "regularity/unit_test_3.txt":
            print("Regularity on Itself                     : ", re.regularity_extraction([0, 1, 2, 3], [0, 1, 2, 3]))
            print("===========================================================================================")
            print("Regularity on Similar Template           : ", re.regularity_extraction([0, 1, 2, 3], [8, 9, 10, 11]))
            print("===========================================================================================")
            print("Regularity on Partial Template           : ", re.regularity_extraction([0, 1, 2, 3], [4, 5, 6, 8]))
            print("===========================================================================================")
            print("Regularity on Dissimilar Template        : ", re.regularity_extraction([0, 1, 2, 3], [5, 6, 7, 9]))

    # Ripple
        case "regularity/pseudo_adder.txt":
            print("Regularity on Itself                     : ", re.regularity_extraction([0, 1, 2, 3, 4], [0, 1, 2, 3, 4]))
            print("===========================================================================================")
            print("Regularity on Similar Template           : ", re.regularity_extraction([0, 1, 2, 3, 4], [5, 6, 7, 8, 9]))
            print("===========================================================================================")
            print("Regularity on Partial Template           : ", re.regularity_extraction([0, 1, 2, 3, 4], [5, 6, 7, 8, 10]))
            print("===========================================================================================")
            x = [random.randint(0, len(re.prep_data) - 1) for _ in range(5)]
            print("Regularity against ", x ,"   : ", re.regularity_extraction([0, 1, 2, 3, 4], x))
            print("===========================================================================================")
            print("Regularity on Dissimilar Template        : ", re.regularity_extraction([0, 1, 2, 3, 4], [7, 8, 9, 10, 11]))
            print("\n")

            print("Regularity on Larger Self                       : ",  re.regularity_extraction([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]))
            print("===========================================================================================")
            print("Regularity on Larger Similar Template           : ", re.regularity_extraction([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], [10, 11, 12, 13, 14, 15, 16, 17, 18, 19]))
            print("===========================================================================================")
            print("Regularity on Larger Partial Template           : ", re.regularity_extraction([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], [5, 6, 7, 8, 9, 10, 11, 12, 13, 15]))
            print("===========================================================================================")
            print("Regularity on Larger Dissimilar Template        : ", re.regularity_extraction([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]))
            print("\n")
            print("===========================================================================================")
            print("Regularity on Max Self :", re.regularity_extraction([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]))

    # re.nets_parse(re.prep_data[0])
if __name__ == "__main__":
    main()