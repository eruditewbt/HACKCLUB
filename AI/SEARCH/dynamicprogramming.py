from transport import *
from printfunction import printSolution
import sys
sys.setrecursionlimit(10000)

def dynamicProgramming(problem):
    cache = {} # state -> futureCost(state)

    best = []

    def futureCost(state, history):
        # Base case
        if problem.isEnd(state):
            best.append(history)
        if state in cache: # Exponential savings
            return cache [state]

        # Actually doing work
        result = min(cost+futureCost(newState, history+[(action, newState, cost)])
            for action, newState, cost in problem.succAndCost(state))
        cache [state] = result
        return result
    return (futureCost(problem.startState(), []), [])#best[0])

### Main
problem = TransportationProblem(N=10)
# print(problem.succAndCost(3))
# print(problem.succAndCost(9))

printSolution(dynamicProgramming(problem))

