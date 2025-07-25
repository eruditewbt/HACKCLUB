import numpy as np

# Modeling: what we want to compute

points=[(np.array([2]),4),(np.array([4]),2)]
d = 1

def F(w):
    return sum((w.dot(x) - y) ** 2 for x, y in points)

def dF(w):
    return sum(2*(w.dot(x) - y) * x for x, y in points)

# Algorithms: how we compute it
def gradientDescent(F, dF, d):
    # Gradient descent
    W = np.zeros(d)
    eta = 0.01
    for t in range(100):
        value = F(w)
        gradient = dF(w)
        w = w - eta * gradient
        print('iteration {}: w = {}, F(w) ={}'.format(t, w, value))

gradientDescent(F, dF, d)