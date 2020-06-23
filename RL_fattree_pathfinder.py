import math
import csv
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import random

k = int(input("Enter a k: "))
pods = k
maxServer = int(math.pow(k,3)/4)
print('CHECK: Max amount of servers given k = ', k, ' is ', maxServer ,'servers')

# first layer, amount of core switches and pods
# pod = set of aggregate switches and number of edge switches

coreCT   = int(math.pow((k/2),2))
interswitch = int(k/2)
servers = int(math.pow((k/2),2))

print('INFO CHECK')
print('Number of Core Switches: ', coreCT, ' and number of inter switches(aggregate and edge switches) : ', interswitch)
print('FAT Tree will be displayed in the following format in numerical fashion:')
print('(PM ID,  EDGE SWITCH,  AGGREGRATE SWITCH, AND CORE SWITCH)')

ft = list()
results=[]

serverID = 0
edgeS = maxServer
aggS  =  maxServer + (2 * servers) -1
coreS = aggS + (2 * servers)
icoreS = coreS
switchCT = 0
aggCT = 0

graph = list()
l1 = list()  # edge between PM_ID => EDGE SWITCH
l2 = list()  # edge between EDGE SWITCH => AGG SWITCH
l3 = list()  # edge between AGG SWITCH => CORE SWITCH

print(aggS, coreS)
for pod in range(0,(k)):
    for a in range(0, (servers)):

        ft.append(serverID)
        l1.append(serverID)
        serverID = serverID + 1
        switchCT = switchCT + 1
        aggCT = aggCT + 1

        if(switchCT <= interswitch):
            ft.append(edgeS)
            l1.append(edgeS)
            aggS = aggS + 1
            ft.append(aggS)
            l2 =[edgeS, aggS]
        else:
            edgeS = edgeS + 1
            ft.append(edgeS)
            l1.append(edgeS)
            switchCT = 1

            if(aggCT >= servers):
                aggS = aggS + 1
                ft.append(aggS)
                aggCT = 1
            else:
                aggS = aggS - (interswitch - 1)
                ft.append(aggS)

        l2 =[edgeS, aggS]

        coreS = coreS + 1

        ft.append(coreS)
        l3 = [aggS, coreS]
        graph.append(tuple(l1))
        graph.append(tuple(l2))
        graph.append(tuple(l3))
        #print(graph)
        results.append(ft)
        print(ft)
        ft, l1, l2, l3 = ([] for i in range(4))

    coreS = icoreS

G = nx.Graph()
G.add_edges_from(graph)
pos = nx.spring_layout(G)
nx.draw_networkx_nodes(G,pos)
nx.draw_networkx_edges(G, pos)
nx.draw_networkx_labels(G,pos)
#plt.show()

maxV = np.max(results) + 1
print(maxV)

source = int(input("Enter the source ID: "))
dest = int(input("Enter the destination ID: "))

R = np.matrix(np.zeros(shape=(maxV,maxV)))
for x in G[dest]:
    R[x,dest] = 100

Q = np.matrix(np.zeros(shape=(maxV,maxV)))
Q -=100
for node in G.nodes:
    for x in G[node]:
        Q[node,x] = 0
        Q[x,node] = 0

pd.DataFrame(R)

def next_number(start, er):
    random_value = random.uniform(0,1)
    if random_value < er :
        if (start > maxServer):
            print(start, G[start])
            sample = G[start]
        else:
            print('thinking..')
            sample = np.where(Q[start,] == np.max(Q[start,]))[1]
    else:
        sample = np.where(Q[start,]==np.max(Q[start,]))[1]
    next_node = int(np.random.choice(sample,1))
    return next_node

def updateQ(n1, n2, lr, discount):
    max_index = np.where(Q[n2,] == np.max(Q[n2,]))[1]
    if max_index.shape[0] > 1:

        max_index = int(np.random.choice(max_index,size=1))
    else:
        max_index = int(max_index)
    max_value = Q[n2, max_index]
    Q[n1,n2] = int((1-lr) * Q[n1,n2] + lr*(R[n1,n2] + discount*max_value))

def learn(er, lr, discount):
       for i in range(50000):
          start = np.random.randint(0, maxV)
          next_node = next_number(start, er)
          updateQ(start, next_node, lr, discount)


learn(0.5, 0.8, 0.8)

pd.DataFrame(Q)
def sp(source, dest):
    path=[source]
    next_node = np.argmax(Q[source,])
    path.append(next_node)
    while next_node != dest:
        print('thinking..next')
        next_node =  np.argmax(Q[next_node,])
        path.append(next_node)
    return path

final_path = sp(source,dest)
print('From', source , 'to', dest, 'takes', len(final_path) - 1  , 'hops!')
print('Final path: ', final_path)

