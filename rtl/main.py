import sys
import pprint
import cost_func as cf
import simulated_annealing as sa
import regularity_extraction as re
import matplotlib.pyplot as plt

def main():

    if (len(sys.argv) != 2):
        print(f"Usage: python3 {sys.argv[0]} <input_file>")
        exit(1)
    input_file = sys.argv[1]

    re.preprocess_data(input_file) 

    # Adder
    V     = [0, 1, 1, 1, 1, 2, 2, 3, 3, 3, 4, 4, 5, 6, 6, 4, 1, 1, 2, 2]
    opt_V = [1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4]

    # print(len(opt_V))
    # print(len(V))

    # 4x4
    V       = [0, 1, 1, 1, 1, 2, 2, 3, 3, 3, 4, 4, 5, 6, 6, 4, 1, 1, 2, 2, 0, 1, 1, 1, 1, 2, 2, 3, 3, 3, 4, 4, 5, 6, 6, 4, 1, 1, 2, 2, 0, 1, 1, 1, 1, 2, 2, 3, 3, 3, 4, 4, 5, 6, 6, 4, 1, 1, 2, 2, 0, 1, 1, 1, 1, 2, 2, 3, 3, 3, 4, 4]
    opt_V   = [1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 0, 5, 5, 6, 6, 6, 6, 6, 7, 7, 7, 7, 7, 8, 8, 9, 9, 10, 10, 10, 10, 10, 11, 11, 11, 11, 11, 12, 12, 12, 12, 12, 13, 13, 14, 14, 15, 15, 15, 15, 15, 16, 16, 16, 16, 16, 17, 17, 17, 17, 17, 0, 0, 0, 0, 0]
    
    # print(len(V))
    # print(len(opt_V))



    print("Simulated Annealing Sol  : ")
    pprint.pprint(sa.simulated_annealing(V, 0.998, 100, 0.001, 50000, 0.55))

    # pprint.pprint(cf.cost_func([5,3,10,9,7,7,11,0,9,10,1,5,8,1,3,6,0,5,0,0,1,1,4,5,0,7,12,6,0,1,11,1,2,3,5,2,14,1,5,0,5,13,5,5, 11,8,4,1,9, 14, 0, 3, 8, 6, 5, 3, 1, 14, 0, 7, 1, 0, 2, 4, 12, 7, 0, 3, 1, 10, 5, 0]))

    # print("Ideal Sol                : ")
    # pprint.pprint([opt_V, cf.cost_func(opt_V)])
if __name__ == "__main__":
    main()