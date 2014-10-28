import sys

def factorial(n):
    if(n>1):
        return n*factorial(n-1)
    else:
        return 1

def fill(results, ntot):

    new_results = []

    if( len(results) == 0 ):
        for i in range(0,ntot):
            new_results.append( i )
    else:
        for el in results:
            print el, i
            for i in range(0,ntot):
                if(i>el):
                    new_results.append( [el, i] )

    return new_results
    
def main(argv):

    ntot = int(argv[0])
    n    = int(argv[1])

    ncomb =  factorial(ntot)/factorial(n)/factorial(ntot-n)
    count = 0
    results   = []

    for i in range(0,n):
        results = fill(results, ntot)

    print results
if __name__ == "__main__":
    main(sys.argv[1:])
