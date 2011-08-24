'''
An example illustrating the use of the __eq__, __cmp__, and __hash__ 
functions for user-defined objects.

Created on 2011-08-19

@author: aparkin
'''

class Foo(object):
    '''
    User defined class.  By default eq, cmp, and hash get default 
    implementations which do comparison based upon reference (ie two objects
    are equal if they are the same instance, and not equal otherwise)

    To override this behaviour one provides implementations for the __eq__
    and/or __cmp__ methods as appropriate.  They are roughly analogous to the
    equals() and compareTo() methods in Java. 

    And as is typically the case in other languages (like Java), if one 
    overrides __eq__, then one should also override __hash__ which returns
    an integer such that for any two instances for which __eq__ returns true,
    __hash__ should return the same hashcode.
    '''
    
    def __init__(self, val):
        self.val = val
        
    def __cmp__(self, other):
        '''
        Typical compareTo style function, return 0 if the two objects are 
        equal, 1 if self is > other, and -1 if self < other.
        '''
        return cmp(self.val, other.val)
    
    def __eq__(self, other):
        '''
        Typical equalTo style method, return True if self and other are 
        equivalent, False otherwise
        '''
        return cmp(self, other) == 0
    
    def __hash__(self):
        '''
        Return a hashcode for this object.  This is used when adding instances
        to a dictionary or set.

        A common trick when one has multiple instance attributes is to put all 
        values inside the object into a tuple, and return the hash of that 
        tuple (since tuples themselves are hashable).
        '''
        return hash(self.val)
    
if __name__ == "__main__":
    # add two equivalent instances to a set, if eq & hash are overridden 
    # properly we should only end up with 1 item in the set.
    s = set([Foo(10), Foo(10)])
    print len(s) # should print 1

    x1 = Foo(10)
    x2 = Foo(10)
    
    print x1 == x2  # returns True (calls __eq__)
    print x1 is x2  # returns False (is does reference equality always)
    print x1 != x2  # returns False (calls __eq__)

    # if eq is defined, then the in operator works as expected
    print Foo(10) in [Foo(10)]   # print true

    print cmp(Foo(10), Foo(10)) # returns 0
    print cmp(Foo(10), Foo(11)) # returns -1 
    print cmp(Foo(11), Foo(10)) # returns 1 

    # sorting of course makes use of the cmp function
    list_of_foos = []
    list_of_foos.append(Foo(5))
    list_of_foos.append(Foo(3))
    list_of_foos.append(Foo(18))
    list_of_foos.append(Foo(-4))

    print "Before sort:"
    for foo in list_of_foos:
        print ("%d, " % foo.val),
    list_of_foos.sort()
    print "\nAfter sort:"
    for foo in list_of_foos:
        print ("%d, " % foo.val),

    print
