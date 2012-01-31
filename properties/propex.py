'''
In most OO settings you often have to write getters and setters for each 
attribute of your class.  This "boilerplate" code tends to be rather tedious
to write.

Python provides an alternative known as properties where you can associate
methods with an attribute of the class for getting, setting, or even deleting
attributes.  

Created on 2012-01-30

@author: aparkin
'''

class Foo(object):
    ''' Example showing off class properties '''
    def __init__(self):
        self.__rwval = 42
        self.__roval = 99
    
    def __get_rwprop(self):
        ''' getter for the __rwval attribute '''
        return self.__rwval
    
    def __set_rwprop(self, xin):
        ''' setter for the __rwval attribute '''
        self.__rwval = xin

    def __get_roprop(self):
        ''' getter for the __roval attribute '''
        return self.__roval
    
    # to define a property we use the property function whose signature is:
    # property(fget=None, fset=None, fdel=None, doc=None)
    
    # define a property called "readwriteprop", and specify the getter and 
    # setter for that property
    readwriteprop = property(__get_rwprop, __set_rwprop)
    
    # define a property called "readonlyprop", and specify the getter for it
    readonlyprop = property(__get_roprop)
    
    # note that the fdel argument to property allows one to provide mechanisms
    # for deleting properties (the usefulness of this is a bit unclear)  
    # Omitting this argument means that the property can no longer be deleted
    # with del
    
    # note as well that now we could change the internal names of the variables
    # containing the data (self.__rwval and self.__roval) and client code would
    # not have to change at all.

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
