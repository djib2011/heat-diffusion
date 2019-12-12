import time
import warnings
from scipy.sparse import lil_matrix # @UnusedImport
import pickle# @UnusedImport
import csv
import collections


def uniqueValues(aList):   
    uniqueStrings = []
    for val in aList:
        isUnique = True
        for unq in uniqueStrings:
            if val == unq:
                isUnique = False
        if isUnique == True:
            uniqueStrings.append(val)
    return uniqueStrings       
def uniqueValues2(aList):
    l = len(aList)
    i = 0
    while i < l:
        j = i
        while j < l:
            if aList[i] == aList[j] and i != j:
                del aList[j]
                l -= 1
                j -= 1
            j += 1
        i += 1   
    return aList    
    '''
    for i in xrange(l):
        for j in xrange(l):
            if aList[i] == aList[j]:
                del aList[j]
                print 'del'
                l -= 1
        #if i in range(1,l,l//100):
            #print( '%i Percent: %s seconds' %( (i//(l//100)), time.time() - startTime) )
        #i += 1
    '''
    
    
    
def mapper(uniqueList):
    startTime = time.time()
    diction = collections.OrderedDict() 
    i=1
    l = len(uniqueList)
    for st in uniqueList:
        diction[st] = i
        i += 1
        if i in range(l//10,l,l//10):
            print( '%i Percent: %s seconds' %( (i*100//l + 1), time.time() - startTime) )
    return diction



time1 = time.time()
print('Reading CSV file:')
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    with open('AOL15000.csv', 'rb') as tempFile:
        reader = csv.reader(tempFile)
        q = []
        l = []
        for row in reader:
            if (row[0] != '') and (row[1] != ''):
                q.append(row[0])
                l.append(row[1])
    time2 = time.time()
    print( 'Read Time: %s seconds' %(time2 - time1) )
    print('Finding Unique Queries:')
    uq = uniqueValues(q)
    time3 = time.time()
    uq2 = uniqueValues2(q)
    time4 = time.time()
    
    print len(uq), len(uq2)
    print set(uq) == set(uq2)
    print time3-time2, time4-time3
    
    
    
    '''
    print('Mapping Queries:')
    global Q
    Q = mapper(uq)
    #pickle.dump(Q, open('queryMap', 'wb'))
    print('Finding Unique URLs:')
    ul = uniqueValues(l)
    print('Mapping URLs:')
    global L
    L = mapper(ul)
    #pickle.dump(L, open('urlMap', 'wb'))
    time3 = time.time()
    '''

   
'''   
time1 = time.time()
uq = uniqueValues(q)
time2 = time.time()
uq2 = uniqueValues2(q)
time3 = time.time()   
print len(uq), len(uq2)
print set(uq) == set(uq2)
print time2-time1, time3-time2
'''


