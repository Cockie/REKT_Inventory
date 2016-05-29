import math
def nCr(n,r):
    f = math.factorial
    #return f(n) / f(r) / f(n-r)
    res = 1
    for i in range(n,n-r-1,-1):
        res*=i
    return res/f(r)

h = []


def loop(c, s, sumi, index):
    global h
    if index >s-1:
        res = h[c-index]
    elif index==s-1:
        res = 0
        for i in range(0, c-s-sumi+1):
            res+= h[i]*h[c-s-sumi-i]
    else:
        res = 0
        for i in range(0, c - s - sumi+1):
            res+=h[i]*loop(c, s, sumi+i,index+1)
    return res

def h_(n,c):

    if c==0:
        return 1
    elif c==1:
        return n
    else:
        res = 0
        for s in range(1,c+1):
            res +=nCr(n, s) * loop(c,s,0,1)
            #maybe switch? idunno
        return res
def htot(n,c):
    global h
    h = [0]*(c+1)
    for i in range(0,c+1):
        print(i)
        h[i] = h_(n,i)
        print(h[i])
        print("--------------")
        #print("h "+str(h[i]))
    return h[c]

#c = 1
for n in range(1,6):
    print("h"+str(n)+",1 "+str(htot(n,1)) + " ?= "+str(n))
#c = 2
for n in range(2, 6):
    print("h"+str(n)+",2 "+str(htot(n,2)) + " ?= "+str(n/2.*(3*n-1)))
#c = 3
for n in range(3, 8):
    print("h"+str(n)+",3 "+str(htot(n,3)) + " ?= "+str(n/3.*(8*n*n-6*n+1)))
#c = 4
for n in range(4, 8):
    print("h"+str(n)+",4 "+str(htot(n,4)) + " ?= "+str(n/4.*(125./6*n*n*n-25*n*n+55./6*n-1)))

print(htot(3600,50))