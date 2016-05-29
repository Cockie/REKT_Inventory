#from Tools.Scripts.treesync import raw_input


classes = []
characters = []
stats = []
assignedClasses = []
classNames = ["Combat", "Survival", "Support", "Recon"]
classes.append([[0, 9, 9, 9, 9, 9, 9, 9], [9, 9, 9, 0, 0, 0, 9, 9, 9]])
classes.append([[9, 0, 0, 9, 9, 9, 9, 9], [0, 0, 9, 9, 9, 9, 9, 9, 9]])
classes.append([[9, 9, 9, 0, 0, 0, 9, 9], [9, 9, 0, 9, 9, 9, 9, 9, 9]])
classes.append([[9, 9, 9, 9, 9, 9, 0, 0], [9, 9, 9, 9, 9, 9, 9, 0, 0]])

with open('char_stats.txt', 'r') as fileNew:
    fileContents = fileNew.read().splitlines()

fileNew.close()

for i in range(0,len(fileContents), 4):
    characters.append(fileContents[i])
    stats.append([fileContents[i + 1].split(","), fileContents[i + 2].split(",")])

for i in range(0,len(characters)):
    results = []
    best = -2
    bestCt = 0
    for q in range(0,len(classes)):
        current = 0
        for q1 in range(0, 2):
            for q2 in range(0, 8):
                current += (min(0, classes[q][q1][q2] - int(stats[i][q1][q2])) * -1)
        if current > best:
            best = current
            bestCt = q
        results.append(current)
    addClass = classNames[bestCt]
    for q in range(0, 4):
        if results[q] > (float(best) * 0.5) and q != bestCt:
           addClass += "-" + classNames[q]

    assignedClasses.append(addClass)

for i in range(0,len(characters)):
    print(characters[i] + ": " + assignedClasses[i])
