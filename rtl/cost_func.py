import regularity_extraction as re

def cost_func(V):
    # print("Current V: ", V, "\n")
    subgraph = [[] for _ in range(max(V) + 1)]
    for i in range(len(V)):
        if (V[i]) == 0:
            continue
        else:
            subgraph[V[i]].append(i)

    compression_eq = 0
    cmpr_cnt = 0
    for i in range(1, len(subgraph)):
        for j in range(i+1, len(subgraph)):
            cmpr_cnt += 1
            if (len(subgraph[i]) == 0) or (len(subgraph[j]) == 0):
                continue
            else:
                compression_eq += re.regularity_extraction(subgraph[i], subgraph[j])

    return (compression_eq / cmpr_cnt) if cmpr_cnt else 0 #Averages

def compression_comparison(U, V):
    cmpr_U = cost_func(U)
    cmpr_V = cost_func(V)

    if (cmpr_U > cmpr_V):
        return U
    else:
        return V
    