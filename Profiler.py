#gametime makes the Profiler wait to start counting actions until after the user has activited the logger
#it knows that recording has started by looking for the row in the TSV that lists the screen resolution
gametime = False
#gamename limits the Profiler to counting events that are happening in the same window, so if someone switches to another application, it won't affect the counts
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
        # this condition flips the gametime switch once the resolution row appears
        # until this happens it won't do anything with any of the log data.
        if gametime == False:
            if row[0] == 'Resolution':
                xresolution = row[1]
                yresolution = row[2]
                xunit = int(xresolution)/16
                yunit = int(yresolution)/12
                gametime = True
        # the else condition will kick in once gametime is True
        else:
            # this converts the time value to a number
            row[2] = int(row[2])
            # the first time that this condition is True, the gamename value will be set to the Window name
            if gamename == '':
                gamename = row[0]
            # after this is set, only actions in the same Window will be acted upon:
            else:
                if row[0] == gamename:
                    # this works on key down actions
                    if row[1] == 'key down':
                        # if the name of the key already exists within the actions dictionary...
                        if row[3] in actions:
                            # then the Time of the key press is added to the array for that key
                            actions[row[3]].append(row[2])
                            # and the actioncounts dictionary value for that key is increased by one
                            actioncounts[row[3]] += 1
                        # if the key hasn't been used yet...
                        else:
                            # then a dictionary entry is created (note that the value is an array with one initial value)
                            actions[row[3]] = [row[2]]
                            # and an actioncounts key is created and initialized
                            actioncounts[row[3]] = 1
                    # this works on key up actions and effectively is a mirror image of the key up actions
                    elif row[1] == 'key up':
                        if row[3] in unactions:
                            unactions[row[3]].append(row[2])
                            unactioncounts[row[3]] += 1
                        else:
                            unactions[row[3]]=[row[2]]
                            unactioncounts[row[3]] = 1
                    # anything that is being recorded that is not a key down/key up is a mouse event, which are recorded a bit differently
                    # luckily after the keyboard eventualities have been eliminated we can just use an else condition
                    else:
                        # the way that pyhook captures mouse clicks, it doesn't record the mouse button in the same way as keyboard key
                        # splits takes the mouse event and breaks it up into an array
                        splits = row[1].split(" ")
                        # the actionname is then determined by the first two words, e.g. "mouse left" as a stand in for the name of the key
                        actionname = splits[0] + " " + splits[1]
                        # row[3] for mouse events is the screen coordinates; the translate method removes the parenthesis that encompass the x, y
                        coords = row[3].translate(None, '()')
                        # then they're split on the comma space into a two value array
                        coords = coords.split(", ")
                        # after the first two words, such as mouse left, mouse right, etc., the third word is up or down
                        if splits[2] == 'down':
                            # this piece here is an early attempt at recording where on the screen the clicks are happening
                            clickx = int(round(int(coords[0])/xunit, 0))
                            clicky = int(round(int(coords[1])/yunit, 0))
                            rawclicks.append([clickx, clicky])
                            # this mirrors the key down recording
                            if actionname in actions:
                                actions[actionname].append(row[2])
                                actioncounts[actionname] += 1
                            else:
                                actions[actionname] = [row[2]]
                                actioncounts[actionname] = 1
                        elif splits[2] == 'up':
                            # while this mirrors the key up recording
                            if actionname in unactions:
                                unactions[actionname].append(row[2])
                                unactioncounts[actionname] +=1
                            else:
                                unactions[actionname] = [row[2]]
                                unactioncounts[actionname] = 1
                                
                            

# this printout is unneccessary for the function
print 'Action(s):'
print actioncounts

# this loop takes each key in the actioncounts dictionary and creates a value in the durations dictionary
for x in actioncounts:
    durations[x] = []
    # it then zips together the Time values for that key's down and up actions...
    temp = zip(actions[x], unactions[x])
    # and for each tuple, it adds the difference between the key up and the key down to the durations array value
    for z in range(len(temp)):
        z1, z2 = temp[z]
        durations[x].append(z2-z1)

# this loop then takes the raw duration values and counts the total time a key was depressed and stores that in durationcounts
# and also determines the average length by dividing the total length of time by the quantity of keypresses
for x in durations:
    instances = 0
    timespan = 0
    for z in durations[x]:
        instances +=1
        timespan += z
    durationcounts[x] = timespan
    durationaverages[x] = timespan/instances

# this printout is unneccessary for the function
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
