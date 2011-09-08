'''
Examples showing off different types of comprehensions in Python (list, set, 
dict, etc)
'''


def main():
    # example of a list comprehension, a list comprehension is typically used
    # in a case where a list is built using a for loop, like so:
    some_list = []
    for item in range(5):
        some_list.append(item)

    # produces the list [0,1,2,3,4], which could alternatively be done as:
    some_list = [ item for item in range(5) ]
    print "some_list: %s" % some_list 
    
    # list comprehensions are also more effecient than for loops.  And we
    # can also introduce things like guards and manipulating functions to
    # do more complex stuff:
    even_nums_doubled = [ num * 2 for num in range(10) if num % 2 == 0 ]
    print "even nums doubled: %s" % even_nums_doubled
    
    # produces the list [ 0, 4, 8 ]

    # If using Python 2.7 or later, We can also use similar notation to 
    # produce sets rather than lists:
    even_nums_doubled = { num * 2 for num in range(10) if num % 2 == 0 }
    print "even nums doubled: %s" % even_nums_doubled
    print "type of even nums: %s " % type (even_nums_doubled)
    
    # note that the only difference is the use of curly braces instead of 
    # square brackets.

    # similarly we can define dictionaries using a similar syntax:
    my_dict = { k : v for k,v in zip (range(5), "Adam is a good guy".split()) }
    print my_dict


if __name__ == "__main__":
    main()
