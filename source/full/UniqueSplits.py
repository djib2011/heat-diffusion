import time
import warnings
import pickle
import csv
import collections


def uniqueValues(aList):   
    uniqueStrings = []
    i = 0
    for val in aList:
        isUnique = True
        for unq in uniqueStrings:
            if val == unq:
                isUnique = False
        if isUnique:
            uniqueStrings.append(val)
        i += 1
    return uniqueStrings


def uniqueCompare(mainList, secondaryList):
    for val in secondaryList:
        if val not in mainList:
            mainList.append(val)
    return mainList


def mapper(uniqueList):
    startTime = time.time()
    diction = collections.OrderedDict() 
    i=1
    l = len(uniqueList)
    for st in uniqueList:
        diction[st] = i
        i += 1
        if i in range(l//10, l, l//10):
            print('%i Percent: %s seconds' % ((i*100//l + 1), time.time() - startTime))
    return diction


def chunks(l, n):
    # Yield successive n-sized chunks from l
    for i in range(0, len(l), n):
        yield l[i:i+n]


time1 = time.time()
print('Reading CSV file:')
with open('Progress', 'w') as f:
    f.write('Reading CSV file:\n')

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
    print('Read Time: %s seconds' % (time2 - time1))

    with open('Progress', 'a') as f:
        f.write('Read Time: %s seconds\n' % (time2 - time1))

    # The csv is stored in two large lists, 1=[] with all the queries and l=[] with all the urls.
    # Because it takes too long to find the unique values of the above lists (around 21 days for each list), we break
    # the list into chunks of 150000 with the function chunks --> a total fof 102 parts
    q = list(chunks(q, 150000))
    time3 = time.time()
    print('Splitting Queries: %s seconds' % (time3 - time2))

    with open('Progress', 'a') as f:
        f.write('Splitting Queries: %s seconds\n' % (time3 - time2))
    l = list(chunks(l, 150000))
    time4 = time.time()
    print('Splitting URLs: %s seconds' % (time4 - time3))

    with open('Progress', 'a') as f:
        f.write('Splitting URLs: %s seconds\n' % (time4 - time3))

    # find the unique values for each sublist q
    uq = uniqueValues(q[0])
    time5 = time.time()

    print('Finding Unique Queries:')
    with open('Progress', 'a') as f:
        f.write('Finding Unique Queries:\n')
    for i in range(1, 101):
        uq_temp = uniqueValues(q[i])  # the left part is just for naming purposes
        uq = uniqueCompare(uq, uq_temp)  # merge the lists
        print('Step %i of 102: %s seconds' % (i + 1, time.time() - time5))
        with open('Progress', 'a') as f:
            f.write('Step %i of 102: %s seconds\n' % (i + 1, time.time() - time5))
    del q
    print('Mapping Queries:')
    with open('Progress', 'a') as f:
        f.write('Mapping Queries:\n')
    Q = mapper(uq)
    del uq
    time6 = time.time()
    print('Saving Query Map')
    with open('Progress', 'a') as f:
        f.write('Saving Query Map\n:')
    pickle.dump(Q, open('queryMap', 'wb'))
    del Q
    print('Done!')
    with open('Progress', 'a') as f:
        f.write('Done!\n')
    print('Total Query Processing Time: %s seconds' % (time.time() - time1))
    with open('Progress', 'a') as f:
        f.write('Total Query Processing Time: %s seconds\n' % (time.time() - time1))

    # find the unique values for each sublist l
    ul = uniqueValues(l[0])
    time7 = time.time()
    print('Finding Unique URLs:')
    with open('Progress', 'a') as f:
        f.write('Finding Unique URLs:\n')
    for i in range(1, 101):
        ul_temp = uniqueValues(l[i])
        ul = uniqueCompare(ul, ul_temp)
        print('Step %i of 102: %s seconds' % (i + 1, time.time() - time7))
        with open('Progress', 'a') as f:
            f.write('Step %i of 102: %s seconds\n' % (i + 1, time.time() - time7))
    del l
    print('Mapping URLs:')
    with open('Progress', 'a') as f:
        f.write('Mapping URLs:\n')
    L = mapper(ul)
    del ul
    print('Saving URL Map')
    with open('Progress', 'a') as f:
        f.write('Saving URL Map:\n')
    pickle.dump(L, open('urlMap', 'wb'))
    del L
    print('Done!')
    print('Total URL Processing Time: %s seconds' % (time.time() - time6))
    print('--- %s seconds ---' % (time.time() - time1))
    with open('Progress', 'a') as f:
        f.write('Done!\n')
        f.write('Total URL Processing Time: %s seconds\n' % (time.time() - time6))
        f.write('--- %s seconds ---\n' % (time.time() - time1))
