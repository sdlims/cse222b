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

    trials = 3
    probability = np.linspace(0.5, 0.7, 19)
    prob_result = []

    for i in probability:
        result = 0
        for j in range(trials):
            result += sa.simulated_annealing(V, 0.998, 100, 0.001, 50000, i)[1]
        prob_result.append(result / trials)
    
    plt.xlabel("Probability Score")
    plt.ylabel("Sim Annealing Result")
    plt.xticks(probability)
    plt.scatter(probability, prob_result, s = None, c = "r", marker = "D")

    plt.show()
    

if __name__ == "__main__":
    main()