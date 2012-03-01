'''
Various little tricks you can do with functions in Python. Some well-known,
some not so well known.
'''
import functools

# Functions are defined with the def keyword
def foo():
    print "I'm in foo!"

# Functions can return values
def the_answer():
    return 42

# Functions can also take arguments
def gimme_somethin(x):
    print "you gave me " + x

# you can write nested functions
def outer_fn():
    def inner_fn(val):
        print "got " % val
    inner_fn(99)
    inner_fn(88)

# you can pass a function as an argument 
def takes_a_function(some_func):
    print "about to run some_func..."
    some_func(99)
    print "ran some_func..."

takes_a_function(outer_fn)
# prints:
# about to run some_func...
# got 99
# got 88
# ran some_func...

# or return a function as a value 
def return_a_function(x):
    def x_plus_y(y):
        return x + y
    return x_plus_y

fn = return_a_function(42)
fn(5) # prints 47

# you can also create anonymous functions with lambda
def return_a_function_using_lambda(x):
    return lambda y: x + y 

fn = return_a_function_using_lambda(42)  # same as before
fn(5) # prints 47

# you can do variable length parameter lists using *args
def who_knows_how_many(*args):
    for param in args:
        print param

who_knows_how_many(42, "adam", 3.1415) # prints the 3 arguments
who_knows_how_many(88) # prints just 1

# you can do named variable length arguments with **kwargs
def foobar(**kwargs):
    if 'adam' in kwargs:
        print kwargs['adam']
    else:
        print "didn't get adam as an argument"

foobar(adam=42)  # prints 42
foobar(bob=99)  # prints "didn't get adam as an argument"

# arguments can be given default values
def func_with_a_default(myval=99):
    print "I got %s" % myval

# and when they're called the user can omit them
func_with_a_default()  # same as func_with_a_default(99)
func_with_a_default(88)  # specify a value 

# callers can also specify parameters by name:
func_with_a_default(myval=102)  # same as func_with_a_default(102)

# you can also inspect the default values given to a function
def showing_func_defaults(b=99):
    print "b is %s, and the default value for b is %s" % (b, showing_func_defaults.func_defaults[0])

showing_func_defaults(88)
# prints 'b is 88, and the default value for b is 99'

# this trick can be used to test if a value was given to a default parameter
def did_i_get_default(b=object()):
    if b is did_i_get_default.func_defaults[0]:
        print "No value was passed for b"
    else:
        print "a value of %s was passed for b" % b

did_i_get_default() # prints "no value was passed for b"
did_i_get_default(b=88) # prints "a value of 88 was passed for b

# people from a functional programming background may like to know how to 
# do partial function application (currying).  This can be done with the
# partial() routine from functools

def mypow(b, e)
    return b ** e 

two_to_the_power = functools.partial(mypow, b=2)
two_to_the_power(e=4) # returns 16

# note you can "fix" either argument:
squareit = functools.partial(mypow, e=2)
squareit(b=3) # returns 9
