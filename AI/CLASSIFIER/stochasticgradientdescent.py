import numpy as np

# Modeling: what we want to compute

points=[(np.array([2]),4),(np.array([4]),2)]
d = 1

def sF(w, i):
    x, y = points[i]
    return (w.dot(x) - y) ** 2

def sdF(w, i):
    x, y = points[i]
    return 2*(w.dot(x) - y) * x

# how we compute it

def stochasticGradientDescent(sF, sdF, d, n):
    # Stochastic Gradient descent
    w = np.zeros(d)
    eta = 1
    numUpdates = 0
    for t in range(1000):
        for i in range(n):
            value = sF(w, i)
            gradient = sdF(w, i)
            numUpdates += 1
            eta = 1 / numUpdates
            w = w - eta * gradient
    print('iteration {}: w = {}, F(w) = {}'.format(t, w, value))

#gradientDescent(F, dF, d)
stochasticGradientDescent(sF, sdF, d, len(points))