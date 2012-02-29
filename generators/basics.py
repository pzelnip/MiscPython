'''
Examples using generators.  Generators are similar to iterators, however, have
the benefit that not all values are loaded into memory, but evaluated and 
returned on a lazy, as-needed basis.

Useful links:

Generator Tricks for Systems Programmers - @L{http://www.dabeaz.com/generators/}
The Python Yield keyword explained - @L{http://stackoverflow.com/questions/231767/the-python-yield-keyword-explained}
itertools module - @L{http://docs.python.org/library/itertools.html}

@author: aparkin
'''

from itertools import islice, izip
from functools import partial 

def fib():
    '''
    A generator function to return an infinite sequence of fibonacci numbers.
    '''
    fib1 = 1
    yield fib1
    fib2 = 1
    yield fib2
    while True:
        fibcur = fib1 + fib2
        yield fibcur
        fib1 = fib2
        fib2 = fibcur

# Taken from the Python itertools module docs:
# http://docs.python.org/library/itertools.html
def take(n, iterable):
    "Return first n items of the iterable as a list"
    return list(islice(iterable, n))

def main():
    ''' main entry point '''

    # spit out the first 10 fibonacci numbers
    for i, val in izip(range(1, 11), fib()):
        print "%d : %d" % (i, val) 

    # or get them as a list:
    print take(10, fib())

    # alternatively, one can create a generator expression.  This looks like
    # a list comprehension but with ( and ) instead of [ and ]
    for pow in (x ** 2 for x in range(5)):
        print pow, 
    
    # Again, the benefit is that values are created as needed, rather than 
    # all at once.

if __name__ == "__main__":
    main()
