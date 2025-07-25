
### Model (search problem)

class TransportationProblemUpdated(object):
    def __init__ (self, N, weights):
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

class TransportationProblem(object):
    def __init__ (self, N):
        # W = number of blocks
        self.N = N
    def startState(self):
        return 1
    def isEnd(self, state):
        return state == self.N
    def succAndCost(self, state):
        # return list of (action, newState, cost) triples
        result = []
        if state+1 <= self.N:
            result.append( ('walk', state+1, 1))
        if state*2 <= self.N:
            result.append( ('tram', state*2, 2))
        return result

#problem = TransportationProblem(N=10)
# print(problem.succAndCost(3))
# print(problem.succAndCost(9))