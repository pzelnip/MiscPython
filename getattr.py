'''
__getattr__ can be used for some neat tricks like adding derived properties
to an object at runtime, on demand.
'''

def some_complex_calculation():
    print "doing some complex calculation"
    # yeah, not complex, but could be...
    return 42

class Foo(object):
    def __getattr__(self, name):
        print "In __getattr__"
        if name is 'complexprop':
            self.__dict__[name] = some_complex_calculation()

        else:
            raise AttributeError(name)
        return self.__dict__[name]

if __name__ == "__main__":

    f = Foo()
    # calcluate the property once...
    print f.complexprop
    
    # now it's there for future use, that some_complex_calculation() only
    # happens once, and only if it's actually needed.
    print f.complexprop
