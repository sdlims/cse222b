# clear && python3 rtl/test_cf.py regularity/pseudo_adder.txt

import sys
import random
import pprint
import regularity_extraction as re
import cost_func as cf

# For Ripple:
# opt_sol         = [1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4]
# adjacent_sol    = [1, 1, 2, 2, 2, 3, 3, 4, 4, 4, 5, 5, 6, 6, 6, 7, 7, 8, 8, 8]
# one_step_right  = [1, 1, 1, 1, 2, 2, 2, 2, 2, 1, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4]
# one_step_left   = [1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4]
# bad_sol         = [1, 1, 2, 2, 3, 3, 3, 3, 4, 5, 6, 6, 7, 7, 6, 6, 1, 1, 2, 3]

# For 4x4 Mult:
opt_sol                     = [1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 0, 5, 5, 6, 6, 6, 6, 6, 7, 7, 7, 7, 7, 8, 8, 9, 9, 10, 10, 10, 10, 10, 11, 11, 11, 11, 11, 12, 12, 12, 12, 12, 13, 13, 14, 14, 15, 15, 15, 15, 15, 16, 16, 16, 16, 16, 17, 17, 17, 17, 17, 0, 0, 0, 0, 0]
adjacent_sol                = [1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 0, 5, 5, 6, 6, 6, 25, 25, 7, 7, 7, 24, 24, 8, 8, 9, 9, 10, 10, 10, 23, 23, 11, 11, 11, 22, 22, 12, 12, 12, 21, 21, 13, 13, 14, 14, 15, 15, 15, 20, 20, 16, 16, 16, 19, 19, 17, 17, 17, 18, 18, 0, 0, 0, 0, 0]
one_step_right              = [1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 0, 5, 5, 6, 6, 6, 6, 6, 7, 7, 7, 7, 7, 8, 8, 9, 9, 10, 10, 10, 10, 10, 11, 11, 11, 11, 11, 12, 12, 12, 12, 12, 13, 13, 14, 14, 15, 15, 15, 15, 15, 16, 16, 16, 16, 17, 17, 17, 17, 17, 16, 0, 0, 0, 0, 0]
one_step_left               = [1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 0, 5, 5, 6, 6, 6, 6, 6, 7, 7, 7, 7, 7, 8, 8, 9, 9, 10, 10, 10, 10, 10, 11, 11, 11, 11, 11, 12, 12, 12, 12, 12, 13, 13, 14, 14, 15, 15, 15, 15, 15, 16, 16, 16, 16, 17, 17, 17, 17, 17, 17, 0, 0, 0, 0, 0]
bad_sol                     = [1, 1, 2, 2, 3, 3, 3, 3, 4, 5, 6, 6, 7, 7, 6, 6, 1, 1, 2, 3, 1, 1, 2, 2, 3, 3, 3, 3, 4, 5, 6, 6, 7, 7, 6, 6, 1, 1, 2, 3, 1, 1, 2, 2, 3, 3, 3, 3, 4, 5, 6, 6, 7, 7, 6, 6, 1, 1, 2, 3, 1, 1, 2, 2, 3, 3, 3, 3, 4, 5, 6, 6]



def main():
    input_file = sys.argv[1]
    re.preprocess_data(input_file)

    # pprint.pprint(re.prep_data)
    # print("Cost on Test Sol                  :", cf.cost_func([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 6, 6, 6, 6, 6, 7, 7, 7, 7, 7]))
    print("Cost on Optimal Sol                  :", cf.cost_func(opt_sol))
    print("Cost on Adjacent Sol                 :", cf.cost_func(adjacent_sol))
    print("Cost on Slightly-Right Optimal Sol   :", cf.cost_func(one_step_right))
    print("Cost on Slightly-Left Optimal Sol    :", cf.cost_func(one_step_left))
    print("Cost on Bad Sol                      :", cf.cost_func(bad_sol))

if __name__ == "__main__":
    main()