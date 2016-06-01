miscdel = 0
misc = 0
patreondel = 0
patreon = 0
mode = -1
num_lines = sum(1 for line in open('wikiinput.txt'))
with open('wikiinput.txt', 'r') as fileContents:
    for line in fileContents:
        if "Miscellaneous" in line:
            mode = 0
        elif "Patreon" in line:
            mode = 1
        else:
            if mode ==0:
                if "--" in line:
                    miscdel += 1
                misc+=1
            elif mode == 1:
                if "--" in line:
                    patreondel += 1
                patreon+=1


print(str(round((100.0 / float(misc)) * miscdel)) + "% of miscellaneous things done, ")
print(str(round((100.0 / float(patreon)) * patreondel)) + "% of this month's Patreon goals")

