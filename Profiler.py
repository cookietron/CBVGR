gametime = False
gamename = ''
starttime = 0
xresolution = 0
yresolution = 0
xunit = 0
yunit = 0

actions = {}
unactions = {}
durations = {}
actioncounts = {}
unactioncounts = {}
durationcounts = {}
durationaverages = {}

rawclicks = []

import csv
with open('PacManDSX.tsv', 'rb') as f:
    reader = csv.reader(f, delimiter='\t')
    for row in reader:
        if gametime == False:
            if row[0] == 'Resolution':
                xresolution = row[1]
                yresolution = row[2]
                xunit = int(xresolution)/16
                yunit = int(yresolution)/12
                gametime = True
        else:
            row[2] = int(row[2])
            if gamename == '':
                gamename = row[0]
            else:
                if row[0] == gamename:
                    if row[1] == 'key down':
                        if row[3] in actions:
                            actions[row[3]].append(row[2])
                            actioncounts[row[3]] += 1
                        else:
                            actions[row[3]] = [row[2]]
                            actioncounts[row[3]] = 1
                    elif row[1] == 'key up':
                        if row[3] in unactions:
                            unactions[row[3]].append(row[2])
                            unactioncounts[row[3]] += 1
                        else:
                            unactions[row[3]]=[row[2]]
                            unactioncounts[row[3]] = 1
                    else:
                        splits = row[1].split(" ")
                        actionname = splits[0] + " " + splits[1]
                        coords = row[3].translate(None, '()')
                        coords = coords.split(", ")
                        if splits[2] == 'down':
                            clickx = int(round(int(coords[0])/xunit, 0))
                            clicky = int(round(int(coords[1])/yunit, 0))
                            rawclicks.append([clickx, clicky])
                            
                            if actionname in actions:
                                actions[actionname].append(row[2])
                                actioncounts[actionname] += 1
                            else:
                                actions[actionname] = [row[2]]
                                actioncounts[actionname] = 1
                        elif splits[2] == 'up':
                            if actionname in unactions:
                                unactions[actionname].append(row[2])
                                unactioncounts[actionname] +=1
                            else:
                                unactions[actionname] = [row[2]]
                                unactioncounts[actionname] = 1
                                
                            
print 'Action(s):'
print actioncounts

for x in actioncounts:
    durations[x] = []
    temp = zip(actions[x], unactions[x])
    for z in range(len(temp)):
        z1, z2 = temp[z]
        durations[x].append(z2-z1)

for x in durations:
    instances = 0
    timespan = 0
    for z in durations[x]:
        instances +=1
        timespan += z
    durationcounts[x] = timespan
    durationaverages[x] = timespan/instances

print 'Duration Total(s):'
print durationcounts
print 'Duration Mean(s):'
print durationaverages

map = []
for x in range(12):
    map.append([0]*16)

for a in rawclicks:
    ay = a[1]
    mx = map[ay]
    ax = a[0]
    mx[ax] += 1
    map[ay] = mx

for i in map:
    print i
