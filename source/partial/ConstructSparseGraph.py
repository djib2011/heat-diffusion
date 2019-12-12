import csv
import numpy as np
from scipy.sparse import lil_matrix, bmat
import pickle
import collections
import warnings
import time
from sys import getsizeof


def uniqueValues(aList):
    """
    Finds the unique elements in a list.
    :param aList: a python list
    :return: a list of unique elements in the given list
    """
    uniqueStrings = []
    for val in aList:
        isUnique = True
        for unq in uniqueStrings:
            if val == unq:
                isUnique = False
        if isUnique:
            uniqueStrings.append(val)
    return uniqueStrings


def mapper(uniqueList):
    """
    Create an OrderedDict mapping the elements of uniqueList to their indices
    :param uniqueList: a list containing unique elements
    :return: a collections.OrderedDict object
    """
    diction = collections.OrderedDict()
    i = 1
    for st in uniqueList:
        diction[st] = i
        i += 1
    return diction


def constructGraph(dset):
    """
    Parses the dataset which is in a text file and constructs the adjecency matrix.
    :param dset: A text file containing the mappings between queries and urls
    :return: the adjacency matrix
    """
    time1 = time.time()
    with warnings.catch_warnings():  # scipy.sparse raise a lot of DeprecationWarnings
        warnings.simplefilter("ignore")
        with open(dset, 'r') as tempFile:
            reader = csv.reader(tempFile)
            q = []
            l = []
            for row in reader:
                if (row[0] != '') and (row[1] != ''):  # splits the two columns of the document into two lists
                    q.append(row[0])
                    l.append(row[1])
        time2 = time.time()
        print('Read Time: %s seconds' %(time2 - time1) )

        # Lists with unique values:
        uq=uniqueValues(q)
        ul=uniqueValues(l)
        time3 = time.time()
        print('Find Unique Values: %s seconds' %(time3 - time2) )

        n = len(uq)  # number of unique queries
        p = len(ul)  # number of unique urls

        # Map nodes to queries/url:
        global Q 
        Q = mapper(uq)  # create OrderedDicts that map queries to nodes
        global L
        L = mapper(ul)
        del uq, ul
        time4 = time.time()
        print('Mapping Time: %s seconds' %(time4 - time3))

        # Accumulative graph:
        E = lil_matrix((n,p))  # Initialize matrix E. We used a lil_matrix because it's faster to create.
        for i in range(len(q)):
            E[Q.get(q[i])-1,L.get(l[i])-1] += 1  # Create a matrix with query-url mappings that counts their occurrences.
                                                 # The rows correspond to queries, while the columns to the amount of
                                                 # times that someone clicked the url based on that specific query.
        del q, l
        time5 = time.time()
        print( 'Construct Accumulative Matrix: %s seconds' %(time5 - time4) )

        sumQ = np.asarray(E.sum(axis=1))  # Sums the rows. Shows the degree of each query node.
        sumL = np.asarray(E.sum(axis=0))  # Sums the columns. Shows the degree of each url node.
        time6 = time.time()
        print('Find Node Degrees Time: %s seconds' %(time6 - time5) )
        print('Total Time: %s seconds' %(time6 - time1) )

        G = lil_matrix((n, p))  # Adjacency matrix. It's a square matrix with a shape of (n+p)x(n+p), where the first n
                                # lines/columns are the urls. Due to our graph's structure (we have no connections among
                                # q and q or l and l), the top left nxn sub-matrix and the bottom right (from n+1 to n+p)
                                # are empty.

        T = lil_matrix((n,p))  # A transposed version of the bottom left sub-matrix.

        print('Query Weight Association:')
        # G = G.todense() # is WAYYYY faster to compute
        # T = T.todense()

        for i in range(n):
            for j in range(p):
                G[i,j] = E[i,j] / int(sumQ[i])  # computes the query outlinks weights
            if i in range(n // 10, n, n // 10):  # print progress
                print('%i Percent: %s seconds' % ((i*100//n) + 1, time.time() - time6))
        time7 = time.time()

        print('Total Query Weight Association Time: %s seconds' %(time7 - time6))
        print('URL Weight Association:')
        for i in range(n):
            for j in range(p):
                T[i, j] = E[i, j] / sumL.item(j)  # computes the url outlinks weights
            if i in range(n // 10, n, n // 10):  # print progress
                print('%i Percent: %s seconds' % ((i*100//n) + 1, time.time() - time7))

        time8 = time.time()
        print('Total URL Weight Association Time: %s seconds' % (time8 - time7))
        del E, sumQ, sumL

        T = T.transpose()
        time9 = time.time()
        print('Transpose Time: %s seconds' % (time9 - time8))

        print('Matrix Join:')
        G = bmat([[None, G],[T, None]])
        del T
        time10 = time.time()
        print('Matrix Join Time: %s seconds' % (time10 - time9))

        G = lil_matrix(G)
        return G


def retrieveMap(whichMap):
    """
    Returns the OrderedDicts containing the url or query mappings
    :param whichMap: Select which OrderedDict you want "l" for urls, "q" for query.
    :return: The selected OrderedDict
    """
    if whichMap == 'l' or whichMap == 'L' or whichMap == 'url' or whichMap == 'link':
        return L  # returns the OrderedDict containing the url mappings
    elif whichMap == 'l' or whichMap == 'Q' or whichMap == 'query':
        return Q  # returns the OrderedDict containing the url mappings


if __name__ == "__main__":
    startTime = time.time()
    G = constructGraph('AOL150000.csv')
    pickle.dump(Q, open('queryMap5', 'wb'))
    pickle.dump(L, open('urlMap5', 'wb'))
    pickle.dump(G, open('graph5', 'wb'))
    print('Done!')
    print('Matrix Sum : %s' %G.sum())
    print('Graph Size : (%i x %i)' %(G.shape[1], G.shape[1]))
    print('Graph Memory Size: %s bytes' % getsizeof(G))
    print( '--- %s seconds ---' %(time.time() - startTime) )
