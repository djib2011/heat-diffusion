from __future__ import division
import numpy as np
import time
import math
import pickle
from scipy import sparse
from scipy.sparse import csr_matrix
from sys import getsizeof
import warnings


def matrixExponential(matrix, g=1, sparse_comp=True):
    """
    Compute the exponent of a matrix through the power series approximation.

    The parameter g shows how many terms we want to use. The higher g is the better the approximation. It is recommended
    to use g=6, but that would take a very long time to run on, so the default implementation is with four terms. Also
    if g is selected, it won't use a sparse computation and it will take less time but a lot of memory.

    Note: This takes an ENORMOUS amount of time for the full AOL dataset, that's why by default I only use the first
          four terms of the series! (It took me 40 days to run this on a single thread).
    the full
    :param matrix: The matrix whose exponent we want to compute.
    :param g:
    :param sparse_comp: Select whether we want sparse computation or not.
    :return: The result of the matrix exponentiation
    """

    nodes = matrix.shape[1]

    if not sparse_comp:
        E = np.eye(nodes)

        for i in range(1, 6):
            E = E + (np.linalg.matrix_power(matrix, i) * (np.power(g, i))) / math.factorial(i)

        # Regularization:
        E = E * nodes / np.sum(E)

    else:
        E = sparse.eye(nodes)

        startTime = time.time()
        print('Calculating Matrix Exponential:')

        G2 = np.power(matrix, 2) / math.factorial(2)
        t2 = time.time()
        print('Term 2 time: %s seconds' % (t2-startTime))

        G3 = G2.dot(matrix) / math.factorial(3)
        t3 = time.time()
        print('Term 3 time: %s seconds' % (t3-t2))

        G4 = G2.dot(G2) / math.factorial(4)
        t4 = time.time()
        print('Term 4 time: %s seconds' % (t4-t3))

        E = E + G2 + G3 + G4
        t5 = time.time()
        print('Term sum time: %s seconds' % (t5-t4))

    return E


def diffuseHeat(G=None, a=1, t=1):
    """
    Computes the operation of the heat diffusion.
    :param G: Graph
    :param a:
    :param t:
    :return:
    """

    time1 = time.time()

    if not G:
        # Load graph:
        G = pickle.load(open('graph5', 'rb'))
        G = csr_matrix(G)

    time2 = time.time()
    print('Graph Load Time: %s seconds' %(time2 - time1))

    # H - D:
    nodes = G.shape[1]
    H = G.transpose()
    D = sparse.eye(nodes)
    del G

    time3 = time.time()
    print('Exponential Preparation Time: %s seconds' %(time3 - time2))
    f = matrixExponential((H-D), a*t)  # compute the exponent. WARNING: Takes a LOT of time
    del H, D

    print('Total Matrix Exponential Time: %s seconds' %(time.time() - time3))
    return f


if __name__ == "__main__":

    startTime = time.time()
    with warnings.catch_warnings(): # scipy.sparse raises a lot of DeprecationWarnings

        warnings.simplefilter("ignore")
        f = diffuseHeat(None, 1, 1)
        pickle.dump(f, open('diffusionGraph5', 'wb'))

        print('Done!')
        print('Matrix Sum : %s' %f.sum())
        print('Diffused Graph Size : (%i x %i)' %(f.shape[1], f.shape[1]))
        print('Diffused Graph Memory Size: %s bytes' %getsizeof(f))

    print('--- %s seconds ---' %(time.time() - startTime))
