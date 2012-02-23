'''
Decorators are syntactic sugar for writing functions that "wrap" other 
functions.  Decorators can be handy for adding additional behaviour to
a method or function.  The can also be rather conceptually difficult to
grasp, particularly if one is not comfortable with the idea of higher
order functions or closures.

Some links describing decorators:

http://stackoverflow.com/questions/9416947/python-class-based-decorator-with-parameters-that-can-decorate-a-method-or-a-fun
http://stackoverflow.com/questions/6122496/python-is-decorators-for-method-arguments-possible
http://stackoverflow.com/questions/2365701/decorating-python-class-methods-how-do-i-pass-the-instance-to-the-decorator
http://agiliq.com/blog/2009/06/understanding-decorators/

http://stackoverflow.com/questions/739654/understanding-python-decorators
This last link contains an answer by e-satis that is quite possibly the best
answer I've ever seen on a SO question.  Having said that, the answer really
only scratches the surface of decorators.

@author: pzelnip
'''

# show a "simple" decorator example that is a class-based decorator which 
# can decorate a method or a function, and that takes arguments

import functools

class MyDecorator(object):
    def __init__(self, msg):
        self.msg = msg 

    def __call__(self, fn):
        @functools.wraps(fn)
        def decorated(*args, **kwargs):         
            print "Running %s, and the decorator got '%s'" % (fn.__name__, 
                                                            self.msg)
            fn(*args, **kwargs)
            print "Ran %s, and the decorator got '%s'" % (fn.__name__, 
                                                            self.msg)
            print "-" * 80
            
        return decorated

class Foo(object):
    @MyDecorator("foobar!")
    def bar(self, x):
        print "In foo.bar, got %s" % x

@MyDecorator("plain function")
def plain_func(x):
    print "in plain function, got %s" % x

if __name__ == "__main__":
    plain_func(42)
    Foo().bar(99)
