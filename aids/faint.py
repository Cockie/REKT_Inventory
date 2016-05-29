from random import randint
psi = 1
chance = (3+psi)/6
if chance>1:
    chance = 1

maxit = 5000000
arr = [0]*1000
for i in range(0,maxit):
    awake = False
    turns = 0
    while not awake:
        turns+=1
        roll=randint(1,6)+psi+1
        if roll>=5:
            awake = True
    arr[turns]+=1

average = 0
for i in range(1,len(arr)):
    average+=i*arr[i]/maxit
    print("You woke up " + str(round(arr[i]/maxit*100,6 )) + "% of the time after " + str(
        i) + " turn(s), so "+str(round(sum(arr[0:i+1])/maxit*100, 6))+"% of the time after that or less.")
    if sum(arr[0:i+1])/maxit==1:
        break


print("average: "+str(average))