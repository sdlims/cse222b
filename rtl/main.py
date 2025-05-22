import cost_func as cf
import simulated_annealing as se
import regularity_extraction as re
import matplotlib.pyplot as plt

def main():

    if (len(sys.argv) != 3):
        print(f"Usage: python3 {sys.argv[0]} <input_file> <output_file>")
        exit(1)
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    re.preprocess_data(input_file)

    re.regularity_extraction()


if __name__ == "__main__":
    main()