import util
from transport import *
from printfunction import printSolution


def uniformCostSearch(problem):
    frontier = util.PriorityQueue()
    frontier.update(problem.startState(), 0)
    best = []
    while True:
        # Move from frontier to explored
        state, pastCost = frontier.removeMin()
        if problem.isEnd(state):
            return (pastCost, best)
        # Push out on the frontier
        for action, newState, cost in problem.succAndCost(state):
            frontier.update(newState, pastCost+cost)
            best=best+[(action, newState, cost)]

### Main

problem = TransportationProblem(N=100)
# print(problem.succAndCost(3))
# print(problem.succAndCost(9))

printSolution(uniformCostSearch(problem))