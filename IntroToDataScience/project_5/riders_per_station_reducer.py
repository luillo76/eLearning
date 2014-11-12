import sys
import logging

#from util import reducer_logfile
#logging.basicConfig(filename=reducer_logfile, format='%(message)s',
#                    level=logging.INFO, filemode='w')

def reducer():
    '''
    Given the output of the mapper for this exercise, the reducer should PRINT 
    (not return) one line per UNIT along with the total number of ENTRIESn_hourly 
    over the course of May (which is the duration of our data), separated by a tab.
    An example output row from the reducer might look like this: 'R001\t500625.0'

    You can assume that the input to the reducer is sorted such that all rows
    corresponding to a particular UNIT are grouped together.

    Since you are printing the output of your program, printing a debug 
    statement will interfere with the operation of the grader. Instead, 
    use the logging module, which we've configured to log to a file printed 
    when you click "Test Run". For example:
    logging.info("My debugging message")
    '''

    oldKey = None
    totalValue = 0

    for line in sys.stdin:
        # your code here
        data = line.strip().split("\t")
        if len(data) != 2: continue

        key, value = data
        value = float(value)

        if oldKey!=None and oldKey != key:
            print '{}\t{}'.format(oldKey,totalValue)
            totalValue = 0

        oldKey = key
        totalValue += value

    if oldKey != None:
        print '{}\t{}'.format(oldKey,totalValue)

        
reducer()
