'''
Python 3.2 introduced the functools.total_ordering decorator to aid in the 
creation of objects which have the rich comparison methods added (lt, eq, 
etc).

If you provide an __eq__ and any one of the other rich comparison methods,
all others are also provided.

This has also been backported to Python 2.7.

http://code.activestate.com/recipes/576685-total-ordering-class-decorator/
'''

from functools import total_ordering

@total_ordering
class FooBar(object):
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __eq__(self, other):
        return (self.a, self.b) == (other.a, other.b)

    def __lt__(self, other):
        return (self.a, self.b) < (other.a, other.b)

if __name__ == "__main__":
    f1 = FooBar(5, 3)
    f2 = FooBar(5, 4)
    f3 = FooBar(5, 3)

    assert f1 != f2
    assert f1 == f3
    assert f1 == f1
    assert f1 < f2
    assert f1 <= f2
    assert f1 <= f3
    assert f2 > f1
    assert f2 >= f1
