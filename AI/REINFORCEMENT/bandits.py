import math
import random


class BernoulliBandit:
    def __init__(self, probs, seed=None):
        self.probs = list(probs)
        self.rnd = random.Random(seed)

    def pull(self, arm):
        return 1 if self.rnd.random() < self.probs[arm] else 0


def epsilon_greedy(bandit, steps=2000, eps=0.1, seed=None):
    rnd = random.Random(seed)
    n_arms = len(bandit.probs)
    counts = [0] * n_arms
    values = [0.0] * n_arms
    reward_sum = 0

    for _ in range(steps):
        if rnd.random() < eps:
            arm = rnd.randrange(n_arms)
        else:
            arm = max(range(n_arms), key=lambda i: values[i])
        r = bandit.pull(arm)
        reward_sum += r
        counts[arm] += 1
        # incremental mean
        values[arm] += (r - values[arm]) / counts[arm]

    return {"reward": reward_sum, "counts": counts, "values": values}


def ucb1(bandit, steps=2000):
    n_arms = len(bandit.probs)
    counts = [0] * n_arms
    values = [0.0] * n_arms
    reward_sum = 0

    # pull each arm once
    for arm in range(n_arms):
        r = bandit.pull(arm)
        reward_sum += r
        counts[arm] = 1
        values[arm] = r

    for t in range(n_arms, steps):
        def score(i):
            bonus = math.sqrt(2.0 * math.log(t + 1) / counts[i])
            return values[i] + bonus

        arm = max(range(n_arms), key=score)
        r = bandit.pull(arm)
        reward_sum += r
        counts[arm] += 1
        values[arm] += (r - values[arm]) / counts[arm]

    return {"reward": reward_sum, "counts": counts, "values": values}


def thompson_sampling(bandit, steps=2000, seed=None):
    rnd = random.Random(seed)
    n_arms = len(bandit.probs)
    # Beta priors
    a = [1] * n_arms
    b = [1] * n_arms
    reward_sum = 0

    for _ in range(steps):
        samples = [rnd.betavariate(a[i], b[i]) for i in range(n_arms)]
        arm = max(range(n_arms), key=lambda i: samples[i])
        r = bandit.pull(arm)
        reward_sum += r
        if r == 1:
            a[arm] += 1
        else:
            b[arm] += 1

    counts = [a[i] + b[i] - 2 for i in range(n_arms)]
    means = [a[i] / (a[i] + b[i]) for i in range(n_arms)]
    return {"reward": reward_sum, "counts": counts, "posterior_means": means}


