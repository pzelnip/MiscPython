'''
An example illustrating operator overloading in Python, using a 3D Vector class
as an example.
'''
class Vector3(object):
    def __init__(self, x, y, z):
        self.__x = x
        self.__y = y
        self.__z = z        
     
    def __str__(self):
        return "x: %s  y: %s  z: %s" % (self.__x, self.__y, self.__z)
    
    def __eq__(self, other):
        return (self.getx() == other.getx() and 
                self.gety() == other.gety() and
                self.getz() == other.getz())
        
    def __hash__(self):
        return hash (self.to_tuple()) 
    
    def getx(self):
        return self.__x
    
    def gety(self):
        return self.__y
    
    def getz(self):
        return self.__z
    
    def dotprod(self, vec):
        return vec.getx() * self.getx() + vec.gety() * self.gety() + \
            vec.getz() * self.getz()
            
    def scalarmult(self, scalar):
        return Vector3(self.getx() * scalar,
                       self.gety() * scalar,
                       self.getz() * scalar)
            
    def to_tuple(self):
        return (self.getx(), self.gety(), self.getz())
    
    def crossprod(self, vec):
        (x1, y1, z1) = self.to_tuple()
        (x2, y2, z2) = vec.to_tuple()
        return Vector3(y1 * z2 - y2 * z1,
                       z1 * x2 - z2 * x1,
                       x1 * y2 - x2 * y1)
        
    def add(self, vec):
        (x1, y1, z1) = self.to_tuple()
        (x2, y2, z2) = vec.to_tuple()
        return Vector3 (x1 + x2, y1 + y2, z1 + z2)

    def sub(self, vec):
        (x1, y1, z1) = self.to_tuple()
        (x2, y2, z2) = vec.to_tuple()
        return Vector3 (x1 - x2, y1 - y2, z1 - z2)
    
    def length(self):
        return sqrt(self.getx() ** 2 + self.gety() ** 2 + self.getz() ** 2)
    
    # operator overloading functions....

    def __add__(self, other):
        '''
        Overload the + operator to add two vectors together
        '''
        if isinstance(other, Vector3):
            return self.add(other)
        else:
            return NotImplemented
        
    def __sub__(self, other):
        '''
        Overload the - operator to subtract two vectors
        '''
        if isinstance(other, Vector3):
            return self.sub(other)
        else:
            return NotImplemented
        
    def __mul__(self, other):
        '''
        Overload the * operator to return the cross product if the other value 
        is a vector, the scalar product if the other value is a float, int, or
        long
        '''
        if isinstance(other, Vector3):
            return self.crossprod(other)
        elif isinstance(other, float):
            return self.scalarmult(other)
        elif isinstance(other, int):
            return self.scalarmult(other)
        elif isinstance(other, long):
            return self.scalarmult(other)
        else:
            return NotImplemented

def main():
    vec5 = Vector3(5,5,5)
    vec1 = Vector3(1,1,1)
    print vec5
    print vec5.dotprod(vec1)
    print vec5.crossprod(vec1)
    
    print "multOp over: %s" % (vec5 * vec1)  # cross product
    print "multOp ver2: %s" % (vec5 * 3)     # scalar product
    print "multOp ver3: %s" % (vec5 * 3.124) # scalar product
    #print "Op ver4: %s" % (vec5 * "adam")    # not implemented
    
    print "addOp over: %s" % (vec5 + vec1)
    
    print "subOp over: %s" % (vec5 - vec1)
    
if __name__ == "__main__":
    main()
