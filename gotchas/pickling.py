'''
Example illustrating how the maximum recursion limit in Python can be an issue
when pickling objects.

If we have a highly recursive object structure, then to pickle the object 
the pickle() routine will recursively navigate the structure potentially 
triggering a "RuntimeError: maximum recursion depth exceeded" exception.

This also affects any kind of multiprocessing code, as MP'd code must pickle
objects whenever interprocess communication (IPC) is employed (such as returning
a result via a Queue or Pipe)

Created on 2011-08-18

@author: aparkin
'''
from multiprocessing import Pool
import os
import pickle

class Messy(object):
    def __init__(self, child):
        self.child = child
             
def buildmessyrecstruct(depth = 1000):
    ''' Builds a recursive structure of the given depth '''
    res = Messy(None)
    for _ in range(depth):
        res2 = Messy(res)
        res = res2
    return res

if __name__ == "__main__":
    mess = buildmessyrecstruct()
    pkl = open ('test.pkl', 'w')
    try:    
        # will cause max recursion depth exceeded
        pickle.dump(mess, pkl)
    except RuntimeError:
        print "blew up"
    pkl.close()
    os.remove('test.pkl')
    
    # same problem as process pools must pickle objects for IPC, this one's 
    # actually really nasty as there's no way to catch the exception.
    pool = Pool(1)
    try:
        pool.map(buildmessyrecstruct, [1000])  # build one Messy with depth 1000
    except:
        print ("This will never get triggered, as the exception is thrown "
                "in subprocess...")

