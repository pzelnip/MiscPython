'''
All classes defined in Python get a __dict__ attribute by default, which 
contains all the attributes associated with the class instance.  This 
can be modified to great effect for dynamically modifying the makeup of a
class instance at runtime.

However, this comes at a cost: dict()'s use a fair bit of space.  If you 
have many instances of a class, then having a __dict__ for each one can
get prohibitively expensive.  The alternative is to use __slots__.

__slots__ if defined causes Python to only reserve enough space as needed
for any defined attributes for the class.  Therein lies the tradeoff: you
no longer can add attributes dynamically.
'''


class BasicObj(object):
    """
    This basic object by default gets a __dict__, and all attribtues are
    stored there.
    """
    def __init__(self):
        self.foo = 42
        self.__dict__['foo'] = 42 # same as previous statement\

class SlotsObj(object):
    '''
    This object uses slots instead, and thus will save some memory space
    '''
    __slots__ = ['foo']  # define a single attribute

    def __init__(self):
        self.foo = 42
        # note that the presence of __slots__ means that this class does not
        # get a __dict__
        # self.__dict__  # causes an AttributeError

# note that if a class inherits from a class which has __slots__, it will not
# have a __slots__ unless explicitly defined (it instead gets the default
# __dict__ attribute)

class SlotsDerived(SlotsObj):
    def __init__(self):
        # self.__slots__  # causes an AttributeError
        self.foo = 42

if __name__ == "__main__":
    f1 = BasicObj()

    print f1.foo

    f2 = SlotsObj()
    print f2.foo

    # note that with slots you can no longer add attributes at runtime
    # f2.newattr = 29348  # causes an AttributeError
