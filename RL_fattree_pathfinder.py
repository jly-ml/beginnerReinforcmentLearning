import math
import networkx as nx
import pandas as pd
import numpy as np
import random
from time import process_time

k = int(input("Enter a k: "))
maxServer = int(math.pow(k, 3) / 4)
print('CHECK: Max amount of servers given k = ', k, ' is ', maxServer, 'servers')

# initializing
coreCT = int(math.pow((k / 2), 2))
interswitch = int(k / 2)
servers = int(math.pow((k / 2), 2))
edgeS = maxServer
aggS = maxServer + (2 * servers) - 1
coreS = aggS + (2 * servers) - int(interswitch / 2) - 1
if (coreS % 2 != 0):
    coreS = coreS + 1
icoreS = coreS

print('INFO CHECK')
print('Number of Core Switches: ', coreCT, ' and number of inter switches(aggregate and edge switches) : ', interswitch)

# initializing lists to add edges to
ft = list()
results = []

serverID = 0
switchCT = 0
aggCT = 0
Cct = 1
v = 2 * (int(math.log(k,2))-1)

# graph to use later for the search
graph = list()
l1 = list()  # edge between PM_ID => EDGE SWITCH
l2 = list()  # edge between EDGE SWITCH => AGG SWITCH
l3 = list()  # edge between AGG SWITCH => CORE SWITCH

print(aggS, coreS, icoreS, v)
for pod in range(0, (k)):
    for a in range(0, (servers)):
        ft.append(serverID)
        l1.append(serverID)
        serverID = serverID + 1
        switchCT = switchCT + 1
        aggCT = aggCT + 1

        if (switchCT <= interswitch):
            ft.append(edgeS)
            l1.append(edgeS)
            aggS = aggS + 1
            ft.append(aggS)
            l2 = [edgeS, aggS]
            coreS = coreS + v
        else:
            edgeS = edgeS + 1
            ft.append(edgeS)
            l1.append(edgeS)
            switchCT = 1
            Cct = Cct + 1
            coreS = icoreS + v + Cct - 1

            if (aggCT >= servers):
                aggS = aggS + 1
                ft.append(aggS)
                aggCT = 1
            else:
                aggS = aggS - (interswitch - 1)
                ft.append(aggS)

        l2 = [edgeS, aggS]
        ft.append(coreS)
        l3 = [aggS, coreS]
        graph.append(tuple(l1))
        graph.append(tuple(l2))
        graph.append(tuple(l3))
        results.append(ft)
        print(ft)
        ft, l1, l2, l3 = ([] for i in range(4))
    Cct = 0

# convert list graph into an actual graph
G = nx.Graph()
G.add_edges_from(graph)
pos = nx.spring_layout(G)
nx.draw_networkx_nodes(G, pos)
nx.draw_networkx_edges(G, pos)
nx.draw_networkx_labels(G, pos)
# plt.show()

# calculate upper boundary
maxV = np.max(results) + 1
# print(maxV)

source = int(input("Enter the source ID: "))
dest = int(input("Enter the destination ID: "))
pd.set_option("display.max_rows", None, "display.max_columns", None)
start = process_time()

# rewards matrix
R = np.matrix(np.zeros(shape=(maxV, maxV)))
for x in G[dest]:
    R[x, dest] = 100

# Q matrix
Q = np.matrix(np.zeros(shape=(maxV, maxV)))
Q -= 100
for node in G.nodes:
    for x in G[node]:
        Q[node, x] = 0
        Q[x, node] = 0


def next_number(start, er):
    random_value = random.uniform(0, 1)
    if random_value < er:
        print(start)
        if ((start > maxServer)):
            print(start, G[start])
            sample = G[start]
        else:
            print('thinking..')
            sample = np.where(Q[start,] == np.max(Q[start,]))[1]
    else:
        sample = np.where(Q[start,] == np.max(Q[start,]))[1]
    next_node = int(np.random.choice(sample, 1))
    return next_node


def updateQ(n1, n2, lr, discount):
    # print('updating Q...')
    max_index = np.where(Q[n2,] == np.max(Q[n2,]))[1]
    if max_index.shape[0] > 1:
        max_index = int(np.random.choice(max_index, size=1))
    else:
        max_index = int(max_index)
    max_value = Q[n2, max_index]
    Q[n1, n2] = int((1 - lr) * Q[n1, n2] + lr * (R[n1, n2] + discount * max_value))

walk = 100 * (pow(5,int(math.log(k))*2) )  # as k increases, the walks needs to increase as well
print(walk)
def learn(er, lr, discount):
    for i in range(int(walk)):
        # print('walking and learning')
        start = np.random.randint(0, maxV)
        next_node = next_number(start, er)
        updateQ(start, next_node, lr, discount)


# begin the walk
learn(0.4, 0.8, 0.8)


def sp(source, dest):
    path = [source]
    nopath = maxServer * maxServer
    limit_count = 0
    next_node = np.argmax(Q[source,])
    path.append(next_node)
    while next_node != dest:
        print('thinking..next')
        next_node = np.argmax(Q[next_node,])
        path.append(next_node)
    return path


final_path = sp(source, dest)
print('From', source, 'to', dest, 'takes', len(final_path) - 1, 'hops!')
print('Final path: ', final_path)

stop = process_time()
print("Time elapsed: ", (stop - start), ' seconds')
