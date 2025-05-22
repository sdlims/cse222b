import sys
import random
import regularity_extraction as re

def main():
    input_file = sys.argv[1]
    re.preprocess_data(input_file)

    print("Regularity on Itself                     : ", re.regularity_extraction([0, 1, 2, 3, 4], [0, 1, 2, 3, 4]))
    print("Regularity on Identical Template         : ", re.regularity_extraction([0, 1, 2, 3, 4], [5, 6, 7, 8, 9]))
    print("Regularity on Partial Template           : ", re.regularity_extraction([0, 1, 2, 3, 4], [5, 6, 7, 8, 10]))
    x = [random.randint(0, len(re.prep_data) - 1) for _ in range(5)]
    print("Regularity against ", x ,"   : ", re.regularity_extraction([0, 1, 2, 3, 4], x))
    print("Regularity on Dissimilar Template        : ", re.regularity_extraction([0, 1, 2, 3, 4], [7, 8, 9, 10, 11]))
    print("\n")
    print("Regularity on Larger Self                       : ",  re.regularity_extraction([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]))
    print("Regularity on Larger Identical Template         : ", re.regularity_extraction([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], [5, 6, 7, 8, 9, 10, 11, 12, 13, 14]))
    print("Regularity on Larger Partial Template           : ", re.regularity_extraction([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], [5, 6, 7, 8, 10, 11, 12, 13, 14, 16]))
    print("Regularity on Larger Dissimilar Template        : ", re.regularity_extraction([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]))
    print("\n")
    print("Regularity on Max Self :", re.regularity_extraction([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]))

if __name__ == "__main__":
    main()