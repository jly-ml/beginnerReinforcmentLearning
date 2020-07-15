import math
import random
import pandas as pd
from get_infofattreegraph import *
from pathfinder import *


confirmation = 'Y'
while (confirmation == 'Y'):
    k = int(input("Enter a k: "))
    maxServer = int(math.pow(k, 3) / 4)


    vm_pair = int(input('Enter in how many VM pairs you would like: '))
    f = int(input("Enter f: "))

    pm_id = [*range(0,maxServer, 1)]
    #print(pm_id)
    source = []
    dest = []

    total_comm_cost = 0
    for a in range (0, vm_pair):
        pair = random.sample(pm_id, 2)
        source.append(pair[0])
        dest.append(pair[1])

    print('source list: ', source)
    print('dest list: ', dest)
    pd.set_option("display.max_rows", None, "display.max_columns", None)


    graph, maxV = info_fattree_graph(k,maxServer)
    for a in range (0, vm_pair):
        #print(source[a], dest[a])
        total_comm_cost = total_comm_cost + pathfinder(source[a], dest[a], graph, maxServer, maxV,k, f)

    print('Total Communication cost will be:', total_comm_cost)
    confirmation = str(input('Start over? Y/N'  )).upper()
    print(confirmation)