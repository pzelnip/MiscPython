'''
The propex.py example shows the somewhat more verbose way of defining 
properties, however, using decorator like syntax the overhead of writing
properties can be reduced.  This file is equivalent to the propex.py example
but using decorators rather than explicit calls to property().

Created on 2012-02-01

@author: aparkin
'''

class Foo(object):
    ''' Example showing off class properties '''
    def __init__(self):
        self.__rwval = 42
        self.__roval = 99
    
    @property
    def readwriteprop(self):
        ''' A read-write property ''' 
        return self.__rwval

    @readwriteprop.setter
    def readwriteprop(self, xin):
        self.__rwval = xin

    @property
    def readonlyprop(self):
        ''' A read-only property '''
        return self.__roval
    
def main():
    ''' main entry point '''
    
    someobj = Foo()
    
    # note property syntax, rather than method calling
    print someobj.readwriteprop   
    someobj.readwriteprop = 99
    print someobj.readwriteprop
    
    print someobj.readonlyprop
    # note that uncommenting the following line causes an AttributeError
    # exception to occur
    # someobj.readonlyprop = 4923
    
    # note that because a delete method wasn't specified on the property, users
    # can no longer delete the property with del so this line causes an
    # AttributeError exception as well 
    # del someobj.readwriteprop

if __name__ == "__main__":
    main()
