from REINFORCEMENT.bandits import BernoulliBandit, epsilon_greedy, thompson_sampling, ucb1
from REINFORCEMENT.gridworld import GridWorld
from REINFORCEMENT.q_learning import greedy_rollout, q_learning


def demo_bandits():
    bandit = BernoulliBandit([0.2, 0.3, 0.6, 0.5], seed=0)
    print("bandits: true probs =", bandit.probs)
    print("epsilon_greedy:", epsilon_greedy(bandit, steps=2000, eps=0.1, seed=0))
    print("ucb1:", ucb1(bandit, steps=2000))
    print("thompson:", thompson_sampling(bandit, steps=2000, seed=0))


def demo_gridworld():
    env = GridWorld(rows=4, cols=4, start=(0, 0), goal=(3, 3), walls=[(1, 1), (2, 1)])
    q = q_learning(env, episodes=600, seed=0)
    path = greedy_rollout(env, q)
    print("gridworld greedy path:", path)


def main():
    demo_bandits()
    print()
    demo_gridworld()


if __name__ == "__main__":
    main()
