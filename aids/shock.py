from random import randint
shock = 0
panic = 0
faint = 0
nothing = 0

willp = -2
it = 500000
for i in range(0,it):
    roll = randint(1,6)+willp
    roll+=randint(1,6)+willp
    if roll<1:
        level=4
    elif roll==1:
        level=3
    elif roll==2:
        level=2
    elif roll==3:
        level=1
    elif roll>3 and roll<6:
        level=0
    else:
        level=-1
    level+=randint(1,6)-3
    if level<3:
        nothing+=1
    elif level<6:
        panic+=1
    elif level<8:
        shock+=1
    else:
        faint+=1

print("The Character with PSI "+str(willp)+":")
print("went in shock "+str(shock/it*100)+"% of the time")
print("panicked "+str(panic/it*100)+"% of the time")
print("fainted "+str(faint/it*100)+"% of the time")
print("did nothing "+str(nothing/it*100)+"% of the time")
