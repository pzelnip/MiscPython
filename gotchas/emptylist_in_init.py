'''
A classic Python gotcha, the empty list to init problem
'''


class Bad(object):
    def __init__(self, listIn=[]):
        '''
        Very bad practice, the empty list is created once, and the same list
        reference will be assigned upon creation of each Bad instance 
        '''
        self.mylist = listIn
        
class Good(object):
    def __init__(self, listIn=None):
        '''
        Better practice, explicitly test if listIn is None, and create a new
        list for each call to __init__
        '''
        if listIn is None:
            listIn = []
        self.mylist = listIn

if __name__ == "__main__":    
    f = Bad()
    g = Bad()
    f.mylist.append("sdf")
    # note that the list in g has also been modified.  Whoops.
    print "f.mylist: ", f.mylist
    print "g.mylist: ", g.mylist
    print "--------"

    f = Good()
    g = Good()
    f.mylist.append("sdf")
    # note that the list in g has not been modified.  Yippee!
    print "f.mylist: ", f.mylist
    print "g.mylist: ", g.mylist

