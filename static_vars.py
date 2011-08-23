
'''
Some examples of having "state" retained across function calls in Python

That is, examples of simulating static variables in C/C++.

'''

# method 1: a global
myGlobal = 0

def usingglobal():
    # in order to access a global variable, you need to use the global
    # keyword to explicitly indicate that the variable is globally defined
    global myGlobal

    myGlobal += 1
    print "myGlobal is %d" % myGlobal


# method 2: function attributes.  This has the benefit of not using a global
# variable (which is generally bad practice)
def usingfnattr():
    usingfnattr.val += 1
    print "usingfnattr.val is %d" % usingfnattr.val 
usingfnattr.val = 0

# method 3: generators.  This avoids a global, and the need for a declaration 
# outside a function, but isn't always applicable depending on how the value
# is being used
def usinggenerators():
    val = 0
    while True:
        val += 1
        yield val

# method 4: using classes

class UsingClass(object):
    counter = 0

    def __call__(self):
        self.counter += 1
        print "using class: %d" % self.counter

if __name__ == "__main__":
    usingglobal()  # prints 1 
    usingglobal()  # prints 2


    usingfnattr()  # prints 1
    usingfnattr()  # prints 2


    # generators are a bit different:
    foo = usinggenerators().next
    print foo() # prints 1
    print foo() # prints 2

    # using classes, a bit odd.
    f = UsingClass()
    f()
    f()
