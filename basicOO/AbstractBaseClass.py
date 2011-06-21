'''
Example showing how abstract base classes work in Python (2.6 or later)
'''

from abc import ABCMeta, abstractmethod # abstract base classes

class AbstractParser:
    '''
    The abstract base class which defines a general interface.  For this example
    we'll have a "parse" method which all implementing classes of AbstractParser
    must implement.
    '''
    
    # Python 2.6 specific way to define an abstract base class
    __metaclass__ = ABCMeta
    
    def __init__(self):
        print "in abstract class constructor"

    @abstractmethod
    def parse(self, input_sentence):
        '''
        Abstract method that parses the input sentence into a tree-structure
        '''
        pass

class ImplementedParser(AbstractParser):
    '''
    An implementation of the AbstractParser interface.
    '''
    def __init__(self):
        print "in implemented class constructor"
        # call base class init
        AbstractParser.__init__(self)
    
    def parse(self, sentence):
        print "in implemented parse"
        return sentence.split()

if __name__ == "__main__":
    # would be an error -- cannot instantiate an abstract class
    # f = AbstractParser()
    
    f = ImplementedParser()
    print f.parse("this is a sentence")

    # returns true for both tests    
    print isinstance(f, ImplementedParser)
    print isinstance(f, AbstractParser)
