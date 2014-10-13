import sys

def factorial(n):
    if(n>1):
        return n*factorial(n-1)
    else:
        return 1

def main(argv):

    ntot = int(argv[0])
    n    = 3

    ncomb =  factorial(ntot)/factorial(n)/factorial(ntot-n)
    count = 0
    results   = []

    for i in range(0,ntot):
        for j in range(i+1,ntot):
            for k in range(j+1,ntot):
                count += 1
                results.append( [i,j,k] )

    if(ncomb != len(results)):
        print ncomb, " != ", len(results)

    print len(results)
    print results

if __name__ == "__main__":
    main(sys.argv[1:])
