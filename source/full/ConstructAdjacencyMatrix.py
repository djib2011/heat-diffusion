from __future__ import division
import pickle
import warnings
import numpy as np
from scipy.sparse import lil_matrix, bmat, vstack, coo_matrix, csr_matrix
import time

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    print('Loading Accumulative Matrix')
    with open('Progress', 'w') as f:
        f.write('Loading Accumulative Matrix\n')
    time1 = time.time()
    E = pickle.load(open('E', 'rb'))
    time2 = time.time()
    print('Load Time: %s seconds' % (time2 - time1))
    with open('Progress', 'a') as f:
        f.write('Load Time: %s seconds\n' % (time2 - time1))
    sumQ = np.asarray(E.sum(axis=1))[:, 0]
    sumL = np.asarray(E.sum(axis=0))[0]
    n = E.shape[0]
    p = E.shape[1]
    G = np.zeros(p)
    T = np.zeros(p)
    time3 = time.time()
    print('Calculate Outlinks Time: %s seconds' % (time3 - time2))
    print('Creating Query Adjacency Matrix')
    with open('Progress', 'a') as f:
        f.write('Calculate Outlinks Time: %s seconds\n' % (time3 - time2))
        f.write('Creating Query Adjacency Matrix\n')
    for j in range(p):
        G[j] = E[0, j] / sumQ[0]
        T[j] = E[0, j] / sumL[j]
    G = coo_matrix(G)
    T = coo_matrix(T)
    E = coo_matrix(E)
    E = csr_matrix(E)

    for i in range(1, n):
        temp = np.zeros(p)
        Eslice = E[i, :].toarray()[0]
        for j in range(p):
            temp[j] = Eslice[j] / sumQ[i]
        G = vstack([G, temp])
        if i in range(n//100, n, n//100):
            print('%i Percent: %s seconds' % ((i*100//n) + 1, time.time() - time3))
            with open('Progress', 'a') as f:
                f.write('%i Percent: %s seconds\n' % ((i*100//n) + 1, time.time() - time3))
    time3s = time.time()
    print('Saving Query Adjacency Matrix')
    with open('Progress', 'a') as f:
        f.write('Saving Query Adjacency Matrix\n')
    pickle.dump(G, open('G', 'wb'))
    time4 = time.time()
    print('Save Time: %s seconds' % (time4-time3s))
    with open('Progress', 'a') as f:
        f.write('Save Time: %s seconds\n' % (time4-time3s))
    
    print('Creating URL Adjacency Matrix')
    with open('Progress', 'a') as f:
        f.write('Creating URL Adjacency Matrix\n')
    for i in range(1, n):
        temp = np.zeros(p)
        Eslice = E[i, :].toarray()[0]
        for j in range(p):
            temp[j] = Eslice[j] / sumL[j]
        T = vstack([T, temp])
        if i in range(n//100, n, n//100):
            print('%i Percent: %s seconds' % ((i*100//n) + 1, time.time() - time4))
            with open('Progress', 'a') as f:
                f.write('%i Percent: %s seconds\n' % ((i*100//n) + 1, time.time() - time4))
    
    del E, sumQ, sumL
    time4s = time.time()
    print('Saving URL Adjacency Matrix')
    with open('Progress', 'a') as f:
        f.write('Saving URL Adjacency Matrix\n')
    pickle.dump(T, open('T', 'wb'))
    time5 = time.time()
    print('Save Time: %s seconds' % (time5-time4s))
    with open('Progress', 'a') as f:
        f.write('Save Time: %s seconds\n' % (time5-time4s))

    print('Total Matrix Population Time: %s seconds' % (time3s - time3 + time4s - time4))
    with open('Progress', 'a') as f:
        f.write('Total Matrix Population Time: %s seconds\n' % (time3s - time3 + time4s - time4))
    T = lil_matrix(T)
    T = T.transpose()
    G = bmat([[None, G], [T, None]])
    del T
    time6 = time.time()
    print('Matrix Join Time: %s seconds' % (time6 - time5))
    print('Saving Graph')
    with open('Progress', 'a') as f:
        f.write('Matrix Join Time: %s seconds\n' % (time6 - time5))
        f.write('Saving Graph\n')
    pickle.dump(G, open('graph', 'wb'))
    print('Done!')
    print('Matrix Sum : %s' % G.sum())
    print('Graph Size : (%i x %i)' % (G.shape[1], G.shape[1]))
    print('--- %s seconds ---' % (time.time() - time1))
    with open('Progress', 'a') as f:
        f.write('Done!\n')
        f.write('Matrix Sum : %s\n' % G .sum())
        f.write('Graph Size : (%i x %i)\n' % (G.shape[1], G.shape[1]))
        f.write('--- %s seconds ---' % (time.time() - time1))
