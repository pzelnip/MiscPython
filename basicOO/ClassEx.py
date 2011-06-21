'''
Simple example of creating a class, doing inheritance, etc.
'''

class Base (object):
    ''' 
    Base class, newest style is to "inherit" from "object".  If this is omitted,
    then certain information about types is lost.  IIRC in Python 3, the new
    style of inheriting from object will be required. 
    '''
    
    # myattribute is a class attribute, and is shared amongst instances. It gets
    # grey however when a class attribute is immutable. 
    mymutableattr = ["this", "is", "a", "list"]
    mynonmutableattr = "This is a string"

    def __init__(self):
        '''
        __init__ is the constructor for a class
        '''
        # note that any attribute preceded by self is an instance var
        self.myattribute = "specific to a class"
    
    @staticmethod
    def static_meth():
        '''
        staticmethod decorator specifies this method is a function that is
        contained in the class, but has no access to any class specific values.
        Note that staticmethod's do not have any cls or self argument.  Generally
        if you have something that could be a staticmethod, then you're probably
        better off having it as a stand-alone function rather than a method
        defined within a class.
        '''
        print "Base static_meth"
        
    @classmethod
    def class_meth(cls):
        '''
        classmethod decorator specifies this method is a static method like in
        Java/C++, and thus has access to class specific values.
        
        Note that classmethods have a cls argument which is the implicit 
        argument which represents the class this method is associated with
        '''
        print "Base class method"
        print cls.mymutableattr
        print cls.mynonmutableattr
        
    def norm_meth(self):
        '''
        Regular method which can be overridden in derived classes, and can 
        access any class or instance values.
        
        Note that regular methods have a self argument which is analogous to 
        the "this" reference in Java -- it refers to the instance on which this
        method is being called (ie someInst.norm_meth() would mean self is 
        someInst)
        '''
        print "Base normal method"
        print self.myattribute
        print self.mymutableattr
        print self.mynonmutableattr
        
class Derived (Base):
    '''
    Derived class, which inherits from Base.  Note that multiple inheritance is
    possible in Python.
    '''
    
    @staticmethod
    def static_meth():
        print "Derived static_meth"
        
    @classmethod
    def class_meth(cls):
        print "Derived class method"
        # note inherited from Base
        print cls.mymutableattr
        print cls.mynonmutableattr

    def norm_meth(self):
        print "derived normal method"
        print self.myattribute
        print self.mymutableattr
        print self.mynonmutableattr
    
if __name__ == "__main__":
    
    f = Base() # create an instance of Base
    f.static_meth()
    f.class_meth()
    f.norm_meth()
    
    print "----"
    d = Derived() # create an instance of Derived
    d.static_meth()
    d.class_meth()
    d.norm_meth()

    print "----"
    f.mymutableattr.append("object")
    print f.mymutableattr
    # note that mymutableattr in d is changed.
    print d.mymutableattr
    
    # but if the value was immutable it's less clear
    print "----"
    f.mynonmutableattr = "this is a new string"
    print f.mynonmutableattr
    # note that mynonmutableattr in d is not changed.
    print d.mynonmutableattr

