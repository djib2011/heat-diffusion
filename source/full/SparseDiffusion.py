from __future__ import division
import numpy as np
import time
import math
import pickle
from scipy import sparse
from scipy.sparse import csr_matrix
from sys import getsizeof
import warnings


def matrixExponential(matrix, g):
    nodes = matrix.shape[1]
    E = sparse.eye(nodes)
    startTime = time.time()
    print('Calculating Matrix Exponential:')
    with open('Progress2', 'a') as f:
        f.write('Calculating Matrix Exponential:\n')

    G2 = np.power(matrix, 2) / math.factorial(2)
    t2 = time.time()
    print('Term 2 time: %s seconds' % (t2-startTime))
    with open('Progress2', 'a') as f:
        f.write('Term 2 time: %s seconds\n' % (t2-startTime))
    G3 = G2.dot(matrix) / math.factorial(3)
    t3 = time.time()
    print('Term 3 time: %s seconds' % (t3-t2))
    with open('Progress2', 'a') as f:
        f.write('Term 3 time: %s seconds\n' % (t3-t2))
    G4 = G2.dot(G2) / math.factorial(4)
    t4 = time.time()
    print('Term 4 time: %s seconds' % (t4-t3))
    with open('Progress2', 'a') as f:
        f.write('Term 4 time: %s seconds\n' % (t4-t3))
    E = E + G2 + G3 + G4
    del G2, G3, G4
    t5 = time.time()
    print('Term sum time: %s seconds' % (t5-t4))
    with open('Progress2', 'a') as f:
        f.write('Term sum time: %s seconds\n' % (t5-t4))
    return E


def diffuseHeat(G=None, a=1, t=1):
    time1 = time.time()
    if not G:
        # Load graph:
        G = pickle.load(open('graph', 'rb'))
        G = csr_matrix(G)
    time2 = time.time()
    print('Graph Load Time: %s seconds' % (time2 - time1))
    with open('Progress2', 'w') as f:
        f.write('Graph Load Time: %s seconds\n' % (time2 - time1))
    # H - D:
    nodes = G.shape[1]
    H = G.transpose()
    D = sparse.eye(nodes)
    del G
    time3 = time.time()
    print('Exponential Preparation Time: %s seconds' % (time3 - time2))
    with open('Progress2', 'a') as f:
        f.write('Exponential Preparation Time: %s seconds\n' % (time3 - time2))
    mat = matrixExponential((H-D), a*t)
    del H, D
    print('Total Matrix Exponential Time: %s seconds' % (time.time() - time3))
    with open('Progress2', 'a') as f:
        f.write('Total Matrix Exponential Time: %s seconds\n' % (time.time() - time3))
    return mat


if __name__ == "__main__":
    startTime = time.time()
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        mat = diffuseHeat(None, 1, 1)
        pickle.dump(mat, open('diffusionGraph', 'wb'))
        print('Done!')
        print('Matrix Sum : %s' % mat.sum())
        print('Diffused Graph Size : (%i x %i)' % (mat.shape[1], mat.shape[1]))
        print('Diffused Graph Memory Size: %s bytes' % getsizeof(mat))
    print('--- %s seconds ---' % (time.time() - startTime))
    with open('Progress2', 'a') as f:
        f.write('Done!\n')
        f.write('Matrix Sum : %s\n' % mat.sum())
        f.write('Diffused Graph Size : (%i x %i)\n' % (mat.shape[1], mat.shape[1]))
        f.write('Diffused Graph Memory Size: %s bytes\n' % getsizeof(mat))
        f.write('--- %s seconds ---' % (time.time() - startTime))
