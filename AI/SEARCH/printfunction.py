


# transportation problem 
def printSolution(solution):
    totalcost, history = solution
    print('totalcost: {}'.format(totalcost))
    for item in history:
        print(item)
