import time
import warnings
from scipy.sparse import lil_matrix
import pickle
import csv

time1 = time.time()
Q = pickle.load(open('queryMap','rb'))
time2 = time.time()
print('Query Map Load Time: %s seconds' % (time2 - time1))
L = pickle.load(open('urlMap','rb'))
time3 = time.time()
print('URL Map Load Time: %s seconds' % (time3 - time2))
n = len(Q)
p = len(L)

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    print('Reading CSV File')
    with open('AOL.csv', 'rb') as tempFile:
        reader = csv.reader(tempFile)
        q = []
        l = []
        for row in reader:
            if (row[0] != '') and (row[1] != ''):
                q.append(row[0])
                l.append(row[1])
    time4 = time.time()
    print('Read Time: %s seconds' % (time4 - time3))
    E = lil_matrix((n, p))
    m = len(q)
    print('Populating Accumulative Matrix')
    try:
        for i in range(m):
            E[Q.get(q[i])-1,L.get(l[i])-1] += 1
            if i in range(m//20, m, m//20):
                print('%i Percent: %s seconds' % ((i*100//m)+1, time.time() - time4))
    except TypeError:
        pass
    del q, l
    time5 = time.time()
    print('Accumulative Matrix Time: %s seconds' % (time5 - time4))
    print('Saving Accumulative Matrix')
    pickle.dump(E, open('E', 'wb'))
    print('Done!')
    print('Matrix Sum : %s' % E.sum())
    print('Matrix Size : (%i x %i)' % (E.shape[1], E.shape[1]))
    print('--- %s seconds ---' % (time.time() - time1))
