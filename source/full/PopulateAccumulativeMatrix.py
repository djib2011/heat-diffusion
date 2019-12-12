import time
import warnings
from scipy.sparse import lil_matrix
import pickle
import csv
import collections


def uniqueValues(aList):
    uniqueStrings = []
    l = len(aList)
    i = 0
    startTime = time.time()
    for val in aList:
        isUnique = True
        for unq in uniqueStrings:
            if val == unq:
                isUnique = False
        if isUnique:
            uniqueStrings.append(val)
        if i in range(1, l, l//100):
            print('%i Percent: %s seconds' % ((i//(l//100)), time.time() - startTime))
        i += 1
    return uniqueStrings


def mapper(uniqueList):
    diction = collections.OrderedDict() 
    i = 1
    for st in uniqueList:
        diction[st] = i
        i += 1
    return diction


time1 = time.time()
print('Reading CSV file:')
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    with open('AOL.csv', 'rb') as tempFile:
        reader = csv.reader(tempFile)
        q = []
        l = []
        for row in reader:
            if (row[0] != '') and (row[1] != ''):
                q.append(row[0])
                l.append(row[1])
    time2 = time.time()
    print('Read Time: %s seconds' %(time2 - time1))
    print('Finding Unique Queries:')
    uq=uniqueValues(q)
    print('Finding Unique URLs:')
    ul=uniqueValues(l)
    time3 = time.time()
    print('Find Unique Values Time: %s seconds' %(time3 - time2))
    n = len(uq)
    p = len(ul)
    global Q 
    Q = mapper(uq)
    global L
    L = mapper(ul)
    del uq, ul
    time4 = time.time()
    print('Mapping Time: %s seconds' % (time4 - time3))
    E = lil_matrix((n, p))
    print('Populating Accumulative Matrix')
    for i in range(len(q)):
        E[Q.get(q[i])-1, L.get(l[i])-1] += 1
        if i in range(n//10, n, n//10):
            print('%i Percent: %s seconds' % ((i*100//n) + 1, time.time() - time4))
    del q, l
    time5 = time.time()
    print('Accumulative Matrix Time: %s seconds' % (time5 - time4))
    
    print('Done!')
    pickle.dump(Q, open('queryMap', 'wb'))
    pickle.dump(L, open('urlMap', 'wb'))
    pickle.dump(E, open('E', 'wb'))
    print('Matrix Sum : %s' % E.sum())
    print('Matrix Size : (%i x %i)' % (E.shape[1], E.shape[1]))
    print('--- %s seconds ---' % (time.time() - time1))
