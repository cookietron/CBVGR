import csv

# vectortransform takes the log filename and returns a dictionary of the input keys with values for:
# raw count, raw duration, avg count per minute and avg duration per minute
def vectortransform(filename):
    gametime = False
    gamename = ''
    starttime = 0
    endtime = 0
    totaltime = 0
    resultvector = {}
    lastact = ''
    with open(filename, 'rb') as f:
        reader = csv.reader(f, delimiter='\t')
        for row in reader:
            if gametime == False:
                if row[0] == 'Resolution':
                    gametime = True
            else:
                row[2] = int(row[2])
                if gamename == '':
                    gamename = row[0]
                    starttime = row[2]
                else:
                    if row[0] == gamename:
                        if row[1] == 'key down':
                            if row[3] in resultvector:
                                resultvector[row[3]]['count'] += 1
                                resultvector[row[3]]['duration'] -= row[2]
                            else:
                                resultvector[row[3]] = {'count':1, 'duration': 0 - row[2]}
                        elif row[1] == 'key up':
                            resultvector[row[3]]['duration'] += row[2]
                        else:
                            splits = row[1].split(" ")
                            actionname = splits[0] + " " + splits[1]
                            if row[1] != lastact:
                                if splits[2] == 'down':
                                    if actionname in resultvector:
                                        resultvector[actionname]['count'] += 1
                                        resultvector[actionname]['duration'] -= row[2]
                                    else:
                                        resultvector[actionname] = {'count':1, 'duration': 0 - row[2]}
                                elif splits[2] == 'up':
                                    resultvector[actionname]['duration'] += row[2]
                            lastact = row[1]
            endtime = row[2]
    totaltime = (endtime - starttime) / 60000.0
    for i in resultvector:
        resultvector[i]['duration'] /= 60000.0
        resultvector[i]['count_per_m'] = float(resultvector[i]['count']) / totaltime
        resultvector[i]['duration_per_m'] = float(resultvector[i]['duration']) / totaltime
    #print totaltime, 'total time of '+gamename
    return resultvector

# orderedvector takes the result from resultvector and returns a list with the values largest to smallest
# it exists as an attempt to try and compensate for similar gameplay with different key configurations
def orderedvector(resultvector):
    temp = []
    output = []
    total = 0
    for i in resultvector:
        temp.append(resultvector[i]['count_per_m'])
        total += resultvector[i]['count_per_m']
    temp.sort()
    for i in temp:
        output.append(i/total)
    output.reverse()
    return output

# innerproduct is used within the vectorspace model could probably replace with mathlab function?
def innerproduct(x, y):
    output = 0
    if len(x) == len(y):
        for thing in range(len(x)):
            output = output + x[thing] * y[thing]
    return output

# also used within the vector space similarity equation
def vectornorm(x, y):
    xcom = 0
    ycom = 0
    output = 0
    for thing in range(len(x)):
        xcom += x[thing]**2
    for thing in range(len(y)):
        ycom += y[thing]**2
    output = (xcom ** 0.5) * (ycom ** 0.5)
    return output

# applies the vectorspace model to to two vectors
def vectorspace(x, y):
    numerator = innerproduct(x,y)
    denominator = vectornorm(x, y)
    return numerator/denominator

# similarity takes two result vectors and creates lists/vectors with 0s filling in absent values
# then uses those lists/vectors to plug into the vectorspace function and returns the similarity
def similarity(x, y, type):
    commonx =[]
    commony = []
    if type == '':
        for i in range(len(x)):
            commonx.append(x[i])
        for i in range(len(y)):
            commony.append(y[i])
        z = len(commonx) - len(commony)
        if z > 0:
            for i in range(z):
                commony.append(0.0)
        if z < 0:
            for i in range(abs(z)):
                commonx.append(0.0)            
    else:
        for thing in x:
            commonx.append(x[thing][type])
            if thing in y:
                commony.append(y[thing][type])
                del y[thing]
            else:
                commony.append(0)
        for thing in y:
            commonx.append(0)
            commony.append(y[thing][type])
    return vectorspace(commonx, commony)

# garbage function to figure out the total running time of a particular log?
def time_print(x):
    for thing in x:
        y = x[thing]['count_per_m']
        z = x[thing]['count'] / x[thing]['count_per_m']
        print thing, z, y, x[thing]['count']

# this function uses the similarity metrics from two sources and computes the norm of those two
# as an attempt to reach a compound similarity metric
# could probably be expanded to include any number of different metrics
def two_factor(x,y):
    i = similarity(vectortransform(x), vectortransform(y), 'count_per_m')
    j = similarity(vectortransform(x), vectortransform(y), 'duration_per_m')
    k = (i**2+j**2)**0.5
    return x + ' and ' + y + ' are this alike: ' + str(k)

# example comparisons:
print '@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@'
print two_factor('PacManDSX.tsv','SuperHexagon.tsv')
print two_factor('PacManDSX.tsv','Hearthstone2.tsv')
print two_factor('Hearthstone2.tsv', 'PapersPlease.tsv')
print '@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@'

# test of orderedvector usage
print similarity(orderedvector(vectortransform('PacManDSX.tsv')),orderedvector(vectortransform('Hearthstone2.tsv')), '')



