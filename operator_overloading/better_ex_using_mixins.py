'''
Additionally Python supports operator overloading, and (in Python 3) if you 
define one of the "magic methods" you get it's converse defined as well (so
for example, if you define __eq__, then you get a sensible __ne__ defined
which uses it).  Again, this is Python 3 only.

Taking all these ideas further, you can create a mixin class where all 
comparability is defined in terms of one operator, and then in derived
classes, just inherit from the mixin class and define the one operator, and
you get all operators defined.  This file illustrates this.

Note that this is based upon ideas presented in:

http://stackoverflow.com/questions/1061283/lt-instead-of-cmp
'''

class ComparableMixin(object):
    '''
    Define sensible defaults for the base "magic methods" in terms of a 
    less than operator.   Any class which inherits from this and defines a
    __lt__ operator gets sensible defualts for __gt__, __ge__, __ne__, etc

    Note that this assumes Python 3.  If using Python 2.x, then you'll have 
    to add all the other rich comparison methods (__ge__, __ne__, etc)
    '''
    def __eq__(self, other):
        return not (self < other or other < self)

    def __le__(self, other):
        return not other < self

class Foo(ComparableMixin):
    def __init__(self, val):
        self.val = val
        super().__init__()
        
    def __lt__(self, other):
        if not isinstance(other, Foo):
            raise TypeError('Unorderable types Foo() < {}()'.format(type(other)))
        
        return self.val < other.val

if __name__ == "__main__":
    f1 = Foo(42)
    f2 = Foo(99)
    f3 = Foo(42)

    # each spits out True
    print(f1 == f1)
    print(f1 != f2)
    print(f1 == f3)
    print(f1 < f2)
    print(f2 > f1)
    print(f1 <= f3)
    print(f1 <= f2)

    try:
        f1 <= "This is not a Foo"
    except TypeError as e:
        print (e)

