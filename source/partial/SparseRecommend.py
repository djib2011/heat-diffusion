import numpy as np
import pickle
from SparseDiffusion import diffuseHeat
from ConstructSparseGraph import constructGraph, retrieveMap
from scipy.sparse import csr_matrix, csc_matrix
import time
import warnings


def findRecommendations(outSlice, limit, Q, L, fastPropagation, returnLinks, returnQueries):
    """
    Find the top recommendations for a given query
    :param outSlice: Slice from heat propagation matrix
    :param limit: Number of recommendations to return
    :param Q: The OrderedDict containing the query mappings
    :param L: The OrderedDict containing the url mappings
    :param fastPropagation: True for faster computations, False for less memory
    :param returnLinks: If we want to links returned
    :param returnQueries: If we want the queries returned
    :return:
    """
    
    maxHeatQueries = csr_matrix((limit,1)) # csr matrices are faster for row slicing
    maxHeatLinks = csr_matrix((limit,1))
    maxHeatQNodes = csr_matrix((limit,1))
    maxHeatLNodes = csr_matrix((limit,1))
    
    if fastPropagation:  # if we want a faster recommendation, the matrices need to be dense
        outSlice = outSlice.todense()  # this will take the most time
        maxHeatQueries = maxHeatQueries.todense()
        maxHeatLinks = maxHeatLinks.todense()
        maxHeatQNodes = maxHeatQNodes.todense()
        maxHeatLNodes = maxHeatLNodes.todense()

    startTime = time.time()
    print('Finding Top %i Nodes:' %limit)
    for i in range(limit):
        for j in range(n, n+p-1):  # links at the graph from nodes n+1 to n+pp
            if (outSlice[j] > maxHeatLinks[i]) and (j-n+1 not in maxHeatLNodes): # the first condition is for the
                                                                                 # ranking, the second is so that each
                                                                                 # node gets added only once
                maxHeatLinks[i] = outSlice[j]  # store the value
                maxHeatLNodes[i] = j-n+1  # store the node

        for j in range(n):  # queries in the graph from node 1 to n
            if (outSlice[j] > maxHeatQueries[i]) and (j+1 not in maxHeatQNodes):
                maxHeatQueries[i] = outSlice[j]
                maxHeatQNodes[i] = j+1
        print('%i Percent: %s seconds' %((i+1)*100//limit  ,(time.time() - startTime)))

    time2 = time.time()
    print('Total Ranking Time: %s seconds' %(time2 - startTime))

    if not fastPropagation:  # these matrices are small and don't take much space
        maxHeatQNodes = maxHeatQNodes.todense()
        maxHeatLNodes = maxHeatLNodes.todense()

    maxHeatQNodes = maxHeatQNodes.astype(np.int)  # change the nodes to int so that they can be used as indices
    maxHeatLNodes = maxHeatLNodes.astype(np.int)
        
    # Results:
    if returnQueries:  # if we want it to print suggested queries
        i = 0
        recommendations = []  # store the first recommendations as as list
        try:
            while (maxHeatQNodes[i] > 0) and (i<limit):  # end at the limit when there isn't a node with heat > 0
                dictIndex = maxHeatQNodes[i] - 1 
                recommendations.append(Q.items()[dictIndex][0])
                i += 1
        except IndexError:   # IndexError: Index out of bounds  ---  TODO: need to fix this
            pass

        print(recommendations)

    if returnLinks: # if we want it to print suggested urls
        i = 0
        recommendations = []
        try:
            while (maxHeatLNodes[i] > 0) and (i<limit):
                dictIndex = maxHeatLNodes[i] - 1
                recommendations.append(L.items()[dictIndex][0])
                i += 1
        except IndexError:   # IndexError: Index out of bounds   ---  TODO: need to fix this
            pass

        print(recommendations)

    maxHeatQueries = csc_matrix(maxHeatQueries) # convert to CSC matrix for faster column slicing
    maxHeatLinks = csc_matrix(maxHeatLinks)
    relativeHeatNodes = csc_matrix((limit,2))

    queryHeat = outSlice[0:n].sum()  # calculate the total heat in the queries
    linkHeat = 1 - queryHeat  # calculate the total heat in urls (queryHeat +l inkHeat = 1)
    relativeHeatQueries = maxHeatQueries * 100 / queryHeat  # convert the top queries heat to precentages
    relativeHeatLinks = maxHeatLinks * 100 / linkHeat # convert the top links heat to precentages
    relativeHeatNodes[:,0] = relativeHeatQueries  # combine these two
    relativeHeatNodes[:,1] = relativeHeatLinks
    
    return relativeHeatNodes

if __name__ ==  '__main__':

    testQuery = 'lucchese boots'
    r = 5  # Number of recommendations
    returnLinks = True  # do we want recommended links?
    returnQueries = True  # do we want recommended queries?
    loadGraph = False  # True: run everything --- False: run step-by-step (if we've already diffused heat)
    prediffusedGraph = True  # True, if we've run CalculateDiffusion beforehand
    fastPropagation = True  # True, for fast computatuions; False, fast for less memory
    a = 1
    t = 1

    startTime = time.time()

    with warnings.catch_warnings():  # scipy.sparse raises a lot of DeprecationWarnings
        warnings.simplefilter("ignore")

        # Load Data:
        if loadGraph:
            G = constructGraph('AOL50000.csv')
            Q = retrieveMap('Q')  # TODO: fix this later!!!
            L = retrieveMap('L')
        else:
            Q = pickle.load(open('queryMap5', 'rb'))
            L = pickle.load(open('urlMap5', 'rb'))
        n = len(Q)
        p = len(L)

        # Initial Heat:
        initialHeatNode = Q[testQuery]

        # Diffusion:
        if prediffusedGraph:
            f = pickle.load(open('diffusionGraph5', 'rb'))
        else:
            if loadGraph:
                f = diffuseHeat(G)
                del G
            else:
                f = diffuseHeat(None, a, t)
        time2 = time.time()
        print('Elements Loaded: %s seconds' %(time2 - startTime))

        # Heat Propagation:
        h = csr_matrix((n+p,1))
        for i in range(n+p):
            h[i] = f[i, initialHeatNode - 1] # slicing
        del f
        time3 = time.time()
        print('Heat Propagation Time: %s seconds' %(time3 - time2))

        trust = findRecommendations(h, r, Q, L, fastPropagation, returnLinks, returnQueries)
        queryTrust = trust[:,0].toarray().tolist()
        linkTrust = trust[:,1].toarray().tolist()

        if returnQueries:
            print(queryTrust)

        if returnLinks:
            print(linkTrust)

    print( '--- %s seconds ---' %(time.time() - startTime) )
