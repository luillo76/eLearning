#! /usr/bin/python

import numpy as np
import math
import sys

array = []

with open('random.dat', 'r') as f:    
    for line in f:
        line    = line.strip()
        columns = line.split()
        i = int( columns[0] )
        array.append( i ) 

    f.closed

#array.sort()

array2 = []

for i in array:
    n = len(array2)
    jj = 0

    for j in range(0,n):
        if( i < array2[j]): break
        jj = j+1

    array2.insert(jj,i)


print array2
