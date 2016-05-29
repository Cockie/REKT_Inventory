deleted = 0
done = 0
num_lines = sum(1 for line in open('wikiinput.txt'))
with open('wikiinput.txt', 'r') as fileContents:
    for line in fileContents:
        if "LATER" in line:
            break
        elif 'high tier' in line.lower() or 'can wait' in line.lower():
            done-=1
        elif "--" in line:
            deleted += 1
        done+=1


print(str(round((100.0 / float(num_lines)) * deleted)) + "% complete")
print(str(round((100.0 / float(done)) * deleted)) + "% of pre-mission complete")

