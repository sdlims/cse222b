import pprint
import regularity_extraction as re

def cost_func(V):
    subgraph = [[] for _ in range(max(V) + 1)]
    for i in range(len(V)):
        if (V[i]) == 0:
            continue
        else:
            subgraph[V[i]].append(i)
        
    # for i in range(len(subgraph)):
    #     print("Subgraph ", i)
    #     pprint.pprint(re.get_subckt(subgraph[i]))
    #     print("\n")
    compression_eq = 0
    cmpr_cnt = 0
    for i in range(1, len(subgraph)):
        for j in range(i+1, len(subgraph)):
            cmpr_cnt += 1
            if (len(subgraph[i]) == 0) or (len(subgraph[j]) == 0):
                continue
            else:
                # print("Comparing ", subgraph[i], "and", subgraph[j])
                re_out = re.regularity_extraction(subgraph[i], subgraph[j])
                compression_eq += re_out
                # print("Compression Result: ", re_out)

    return (compression_eq / cmpr_cnt) if cmpr_cnt else 0 #Averages

def compression_comparison(U, V):
    cmpr_U = cost_func(U)
    cmpr_V = cost_func(V)

    if (cmpr_U > cmpr_V):
        return U
    else:
        return V
    