import sys
import random
import copy

import numpy as np
import matplotlib.pyplot as plt


def run_simulation(men, women):
    success = 0

    maxm = max(men)
    minw = min(women)

    men2 = []
    women2 = []
    count = 0
    while( maxm > minw and len(men)>0 ):
        count += 1
        random.shuffle( men )
        random.shuffle( women )

#        print "men  ", men
#        print "women", women

        for i in range(0, len(men)):
            if men[i] > women[i]:
                success += 1
            else:
                men2.append( men[i] )
                women2.append( women[i] )

        men   = copy.deepcopy(men2)
        women = copy.deepcopy(women2)
        if(count > 5): break

    return success

def print_results(results):
    print
    print '           Minimum: %s' % (np.amin(results))
    print '   25th Percentile: %s' % (np.percentile(results, 25))
    print '            Median: %s' % (np.median(results))
    print '   75th Percentile: %s' % (np.percentile(results, 75))
    print '           Maximum: %s' % (np.amax(results))
    print
    print '              Mean: %s' % (np.mean(results))
    print 'Standard Deviation: %s' % (np.std(results))
    print '          Variance: %s' % (np.var(results))
    print
    print '           Victory: %s' % (float(sum(i > 20 for i in results)) / len(results))
    print


def plot_results(results):
    plt.hist(results, bins = (np.amax(results) - np.amin(results)), normed = True)
    plt.title('Election Results')
    plt.xlabel('Margin')
    plt.ylabel('Probability')
    plt.show()


def main(argv):

    npersons = int(argv[0])
    men   = []
    women = []

    results   = []

    for _ in range(0,int(argv[1])):
        for _ in range(0,npersons):
            men  .append( random.uniform(0, 200) )
            women.append( random.uniform(0, 200) )

            #print men
            #print women
            results.append( run_simulation(men, women) )


    print_results(results)
#    plot_results(results)


if __name__ == "__main__":
    main(sys.argv[1:])
