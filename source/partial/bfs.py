import numpy as np
import h5py
import pickle
import time


def singleSearch(branch, pruneFactor):
    nodeRank = np.zeros((pruneFactor))
    nodeRanking = np.zeros((pruneFactor))
    response = np.zeros((2, pruneFactor))
    for j in range(pruneFactor):
        for i in range(branch.shape[0]):
            if (branch[i] > nodeRanking[j]) and (i not in nodeRank[:]):
                nodeRank[j] = i
                nodeRanking[j] = branch[i]
    response[0][:] = nodeRank[:]
    response[1][:] = nodeRanking[:]
    return response


def bfs(graph, initNode, searchResults, depth, width):
    r = singleSearch(graph[initNode], width)
    for i in range(depth):
        for j in range(width):
            if r[0][j] in searchResults[0][:] and r[0][j] != 0:
                for k in range(searchResults.shape[1]):
                    if r[0][j] == searchResults[0][k]:
                        searchResults[1][k] += (searchResults[1][k] * r[1][j])
            elif r[0][j] != 0:
                tmp = np.zeros((2, 1))
                tmp[0] = r[0][j]
                tmp[1] = r[1][j]
                searchResults = np.append(searchResults, tmp, axis=1)
        for z in range(1, searchResults.shape[1]):
            bfs(graph, searchResults[0][z], searchResults, depth - 1, width)
    return searchResults


startTime = time.time()

testQuery = 'lucchese boots'
depth = 3
width = 5

with h5py.File('graph2.h5', 'r') as hf:
    data = hf.get('dataset_1')
    G = np.array(data)

Q = pickle.load(open('queryMap2', 'rb'))
L = pickle.load(open('urlMap2', 'rb'))

n = len(Q)
p = len(L)

initialHeatNode = Q[testQuery]
s = initialHeatNode - 1
r = np.zeros((2, width))
# bfs(G, s, r, depth, width)

searchResults = bfs(G, s, r, depth, width)
print (searchResults[0], searchResults[1])

endTime = time.time()
