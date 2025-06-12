import sys 
import pprint
import numpy as np
import matplotlib.pyplot as plt

sys.path.append(r'/home/sdli/regularity_extraction/rtl/')

import cost_func as cf
import simulated_annealing as sa
import regularity_extraction as re

def main():

    if (len(sys.argv) != 2):
        print(f"Usage: python3 {sys.argv[0]} <input_file>")
        exit(1)
    input_file = sys.argv[1]

    re.preprocess_data(input_file) 

    # Adder
    V     = [0, 1, 1, 1, 1, 2, 2, 3, 3, 3, 4, 4, 5, 6, 6, 4, 1, 1, 2, 2]
    opt_V = [1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4]

    trials = 5
    probability = np.arange(0.5, 0.75, 0.025)
    prob_result = []

    for i in probability:
        result = 0
        for _ in range(trials):
            result += sa.simulated_annealing(V, 0.998, 150, 0.001, 50000, i)[1]
        prob_result.append(result / trials)
    
    plt.xlabel("Probability")
    plt.ylabel("Sim Annealing Result")
    plt.xticks(probability)
    plt.scatter(probability, prob_result, s = None, c = "r", marker = "D")

    # result = sa.simulated_annealing(V, 0.9998, 100, 0.001, 50000, 0.625)
    # print("Resulting V          : ", result[0])
    # print("Regularity Extraction: ", result[1])

    # print("Optimal RE: ", cf.cost_func(opt_V))


    # result = sa.simulated_annealing(opt_V, 0.998, 150, 0.001, 75000, 0.625)
    # print("Resulting V          : ", result[0])
    # print("Regularity Extraction: ", result[1])

    plt.show()
    

if __name__ == "__main__":
    main()