# list sub-process modules
import shifter
import collecter
import operator

# list python modules
import multiprocessing

# list variables
# table is a dict
# key   : phase
# item  : control bits
table   = dict()
# log is a dict
# key   : clk
# item  : (phase, control bits) 
log     = dict()
# flag is a queue
# item  : status
flag    = multiprocessing.Queue()

# define main function
# control sub-processes
# run by multi-thread
if __name__ == '__main__':
    p_shifter   = multiprocessing.Process(name='p_shifter',   target=shifter.shift(flag))
    p_collector = multiprocessing.Process(name='p_collector', target=collecter.collect(flag))
    p_operator  = multiprocessing.Process(name='p_operator',  target=operator.operate(flag))

    while (1):
        p_shifter.start()
        p_collector.start()
