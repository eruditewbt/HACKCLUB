#
import sys
sys.setrecursionlimit(10000)

from transport import *
from printfunction import printSolution

def backtrackingSearch(problem):
    # Best solution found so far (dictionary because of python scoping technicality)
    best = {
        'cost': float('+inf'),
        'history': None
    }
    def recurse(state, history, totalCost) :
        # At state, having undergone history, accumulated
        # totalCost.
        # Explore the rest of the subtree under state.
        if problem.isEnd(state):
            # Update the best solution so far
            if totalCost<best['cost']:
                best ['cost'] = totalCost
                best['history'] = history
            return
        # Recurse on children
        for action, newState, cost in problem. succAndCost(state):
            recurse(newState, history+[(action, newState, cost)], totalCost+cost)
    recurse(problem.startState(), history=[], totalCost=0)
    return (best['cost'], best['history'])

### Main

problem = TransportationProblem(N=1000)
# print(problem.succAndCost(3))
# print(problem.succAndCost(9))
printSolution(backtrackingSearch(problem) )

