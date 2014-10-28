#! /bin/python

import sys
import random

import numpy as np
import matplotlib.pyplot as plt

def make_bet(initial_money, gain_goal):
    prob=18.0/37.0

    nbets = 0
    bet = 1
    money = initial_money

    while(True):
        nbets += 1
        youWin = (random.uniform(0,1) < prob)
        if( youWin ):
            money += bet
            bet = 1
        else:
            money -= bet
            bet *= 2

        if( (money-initial_money) >= gain_goal ): break
        if( bet>money ): break

    return nbets, money-initial_money

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
    print


def plot_results(results, xlabel, ylabel, outname):
    
    plt.clf()
    plt.hist(results, bins = (np.amax(results) - np.amin(results)), normed = False, log = True)
    plt.title('')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    #plt.show()
    plt.savefig(outname, format='pdf')

def main(argv):
    ''' Main Function'''
    ntest = int(argv[0])
    initial_money = float(argv[1])
    gain_goal = float(argv[2])
    print " ntest",ntest
    print " initial_money",initial_money
    print " gain goal",gain_goal

    nwins=0

    bets = []
    gains = []

    for i in range(0,ntest):
        nbets, gain = make_bet(initial_money, gain_goal)
        #print nbets, gain
        if(gain>=gain_goal): nwins+=1

        bets.append( nbets )
        gains.append( gain )

    print_results(bets)
    print_results(gains)
    plot_results(bets, '# bets', 'counts', 'bets.pdf')
    plot_results(gains, 'gains', 'counts', 'gains.pdf')

    print nwins
    print "Prob[%] = ", (nwins*100.0)/ntest

if __name__ == "__main__":
    main(sys.argv[1:])


