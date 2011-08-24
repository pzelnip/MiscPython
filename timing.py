
'''
Some examples of using timeit() to time code, example done is finding all even 
numbers in a list of numbers
'''
from timeit import Timer

def byhand(lst):
    res = []
    for elt in lst:
        if elt % 2 == 0:
            res.append(elt)

if __name__ == "__main__":
    
    # method 1: by using filter()
    filtertimer = Timer("""filter(lambda x: x % 2 == 0, range(1000))""")

    # method 2: by user-written function
    userfntimer = Timer("""byhand(range(1000))""", "from __main__ import byhand")

    # method 3: by list comprehension
    listcomptimer = Timer("""[ elt for elt in range(1000) if elt % 2 == 0 ]""")


    # spit out results:
    num_iterations = 10000
    print filtertimer.timeit(num_iterations) # 1000 iterations
    print userfntimer.timeit(num_iterations)
    print listcomptimer.timeit(num_iterations)
