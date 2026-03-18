class GridWorld:
    """
    Simple deterministic gridworld with terminal goal.
    State: (r, c)
    Actions: 0=up,1=right,2=down,3=left
    """

    def __init__(self, rows=4, cols=4, start=(0, 0), goal=(3, 3), walls=None):
        self.rows = rows
        self.cols = cols
        self.start = start
        self.goal = goal
        self.walls = set(walls or [])
        self.state = start

    def reset(self):
        self.state = self.start
        return self.state

    def step(self, action):
        if self.state == self.goal:
            return self.state, 0.0, True

        r, c = self.state
        nr, nc = r, c
        if action == 0:
            nr -= 1
        elif action == 1:
            nc += 1
        elif action == 2:
            nr += 1
        elif action == 3:
            nc -= 1

        # bounds + walls
        if nr < 0 or nr >= self.rows or nc < 0 or nc >= self.cols or (nr, nc) in self.walls:
            nr, nc = r, c

        self.state = (nr, nc)
        done = self.state == self.goal
        reward = 1.0 if done else -0.01
        return self.state, reward, done


