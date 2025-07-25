import sys
sys.setrecursionlimit(10000)
from dynamicprogramming import dynamicProgramming
from A_star import AStar
from backtracking import backtrackingSearch

### Model (search problem)

class TransportationProblem(object):
    def __init__(self, N, weights):
        # N = number of blocks
        # weights = weights of different actions
        self.N = N
        self.weights = weights
    def startState(self):
        return 1
    def isEnd(self, state):
        return state == self.N
    def succAndCost(self, state):
        # return list of (action, newState, cost) triples
        result = []
        if state+1 <= self.N:
            result.append(('walk', state+1, self.weights['walk']))
        if state*2 <= self.N:
            result.append(('tram', state*2, self.weights['tram']))
        return result
    
def predict(N, weights):
    # f(x)
    # Input (x): N (number of blocks)
    # Output (y): path (sequence of actions)
    problem = TransportationProblem(N, weights)
    totalCost, history = dynamicProgramming(problem)
    # totalCost, history = backtrackingSearch(problem)
    return [action for action, newState, cost in history]

def generateExamples():
    trueWeights = {'walk': 1, 'tram': 2}
    return [(N, predict(N, trueWeights)) for N in range(1, 10000)]

def structuredPerceptron(examples):
    weights = {'walk': 0, 'tram': 0}
    for t in range(100):
        numMistakes = 0
        for N, trueActions in examples:
            # Make a prediction
            predActions = predict(N, weights)
            if predActions != trueActions:
                numMistakes += 1
            # Update weights
            for action in trueActions:
                weights [action] -= 1
            for action in predActions:
                weights [action] += 1
        print('Iteration {}, numMistakes = {}, weights = {}'.format(t, numMistakes, weights))
        if numMistakes == 0:
            break

examples = generateExamples()
print('Training dataset:')
for example in examples:
    print(' ', example)
structuredPerceptron(examples)



