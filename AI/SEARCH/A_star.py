import util
from transport import *
from printfunction import printSolution


### Model (search problem)

def heuristic(state, N):
    i=1
    while state<N:
       state+=state
       if state>N:
           break
       i+=2
    return i


def AStar(problem):
    frontier = util.PriorityQueue()
    start = problem.startState()
    frontier.update((start, 0), heuristic(start, problem.N))
    explored = set()
    best = []
    bestState = 0
    while True:
        (state, pastCost), _ = frontier.removeMin()
        if problem.isEnd(state):
            return (pastCost, best)
        if state in explored:
            continue
        explored.add(state)
        for action, newState, cost in problem.succAndCost(state):
            newCost = pastCost + cost
            priority = newCost + heuristic(newState, problem.N) - heuristic(state, problem.N)
            frontier.update((newState, newCost), priority)
            if newState>bestState:
                best=best+[(action, newState, cost , newCost, priority)]
                bestState = newState

### Main

# trueWeights = {'walk': 1, 'tram': 2}
# for N in range(1, 10):
#     problem = TransportationProblemUpdated(N, trueWeights)

# trueWeights = {'walk': 1, 'tram': 2}
# problem = TransportationProblemUpdated(N=10, weights=trueWeights)

problem = TransportationProblem(N=100)
# print(problem.succAndCost(3))
# print(problem.succAndCost(9))

printSolution(AStar(problem))