import random


def q_learning(env, episodes=400, alpha=0.3, gamma=0.98, eps=0.2, seed=None):
    rnd = random.Random(seed)
    q = {}  # (state, action) -> value

    def get_q(s, a):
        return q.get((s, a), 0.0)

    def best_action(s):
        return max(range(4), key=lambda a: get_q(s, a))

    for _ in range(episodes):
        s = env.reset()
        done = False
        while not done:
            if rnd.random() < eps:
                a = rnd.randrange(4)
            else:
                a = best_action(s)
            ns, r, done = env.step(a)
            # bellman target
            target = r + (gamma * max(get_q(ns, na) for na in range(4)) if not done else 0.0)
            q[(s, a)] = (1 - alpha) * get_q(s, a) + alpha * target
            s = ns

    return q


def greedy_rollout(env, q, max_steps=100):
    s = env.reset()
    path = [s]
    for _ in range(max_steps):
        if s == env.goal:
            break
        a = max(range(4), key=lambda aa: q.get((s, aa), 0.0))
        s, _, _ = env.step(a)
        path.append(s)
    return path


