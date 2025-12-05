import os
from transportmdp import TransportationMDP

def valueIteration (mdp) :
    # initialize
    V = {} # state -> Vopt[state]
    for state in mdp.states():
        V[state] = 0.

    def Q(state, action):
        return sum(prob*(reward + mdp.discount()*V[newState])\
            for newState, prob, reward in mdp.succProbReward(state, action))
    
    while True:
        # compute the new values (newV) given the old values (V)
        newV = {}
        for state in mdp.states():
            if mdp.isEnd(state):
                newV [state] = 0.
            else:
                newV [state] = max(Q(state, action) for action in mdp.actions(state))
        # check for convergence
        if max(abs(V[state]-newV[state]) for state in mdp.states())<1e-10:
            break
        V = newV

        # read out policy
        pi = {}
        for state in mdp.states():
            if mdp.isEnd(state):
                pi[state] = 'none'
            else:
                pi[state] = max((Q(state, action), action) for action in mdp.actions(state))[1]

    # print stuff out
    os.system('clear')
    print('{:15} {:15} {:15}'.format('s', 'V(s)','pi(s)'))
    for state in mdp.states():
        print('{:15} {:15} {:15}'.format(state, V[state], pi[state]))
    input()

mdp = TransportationMDP(N=10)
#print(mdp.actions(3))
#print(mdp.succProbReward(3, 'walk'))
#print(mdp.succProbReward(3,'tram'))
valueIteration (mdp)
