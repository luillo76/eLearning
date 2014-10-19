#! /bin/python

import random

def main():
    ''' Main Function'''

states = {}

with open("senate.csv", "r" ) as f:
    f.readline()
    for line in f:
        line = line.strip('\n')
        words = line.split(',')
        if( len(words) != 3):
            print "len(words) = ", len(words)
            exit
        margin = float(words[1])
        error  = float(words[2])
        std    = error / 1.959964

        states[ words[0] ] = (margin, std)

f.close()

#print states

ntest=20000

nwins=0
for i in range(0,ntest):

    nwin = 0

    for state in states:
        mu = states[state][0]
        sigma = states[state][1]
        if( random.gauss(mu, sigma) > 0):
            nwin += 1
#    print nwin

    if( nwin >= 21):
        nwins += 1

print nwins

print "Prob[%] = ", (nwins*100.0)/ntest

if __name__ == '__main__':
    main()

