#! /usr/bin/python

import numpy as np
import math
import sys
import fileinput

letters = {}
letters['a'] = 1
letters['b'] = 2
letters['c'] = 3
letters['d'] = 4
letters['e'] = 5
letters['f'] = 6
letters['g'] = 7
letters['h'] = 8
letters['i'] = 9
letters['j'] = 10
letters['k'] = 11
letters['l'] = 12
letters['m'] = 13
letters['n'] = 14
letters['o'] = 15
letters['p'] = 16
letters['q'] = 17
letters['r'] = 18
letters['s'] = 19
letters['t'] = 20
letters['u'] = 21
letters['v'] = 22
letters['w'] = 23
letters['x'] = 24
letters['y'] = 25
letters['z'] = 26

word = raw_input('What is your name?')

word = word.lower()

a = 0

n = len(word)
for i in range(0,n):
    print word[i], letters[ word[i] ]
    a += letters[ word[i] ]

print a


