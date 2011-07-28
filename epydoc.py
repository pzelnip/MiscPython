'''
Some examples of using Epydoc comments

http://epydoc.sourceforge.net/
'''

class Foo(object):
    def some_method(self, val_in):
        '''
        Usual docstring for a method, but with epydoc stuff. Epydoc
        comments can do I{italicized}, B{bolded}, C{code}, M{math}.

        Lists work too:
        - this is an item
        - this is another
            1. Numbered lists are a bit stupid
            2. As you have to number them manually 

        Url's are done like so: U{Epydoc homepage<http://epydoc.sourceforge.net/>}

        You can also do cool stuff like doctest blocks:

        >>> Foo().some_method(42)
        42

        @param val_in: a description of parameter val_in 
        @type val_in: the type of val_in (int, str, etc)

        @return: a description of the return value of this method
        @rtype: the type of value returned (int, str, etc)

        @raise ValueError: indicate that this function can throw a ValueError
        exception.
        '''
        return val_in


