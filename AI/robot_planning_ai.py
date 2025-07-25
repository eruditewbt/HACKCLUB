class RobotArm4x4:
    def __init__(self):
        self.grid = [[0 for _ in range(4)] for _ in range(4)]
        self.grid[3] = ['A', 'B', 'C', 'D']
        self.holding = 0
        self.ready = True
        self.log = []
        self.position = (0, 0)

    def log_action(self, action):
        self.log.append(action)

    def BOX(self, X):
        return X in ['A', 'B', 'C', 'D']

    def CLEAR(self, X):
        pos = self.find_box(X)
        if not pos:
            return False
        i, j = pos
        return i == 0 or self.grid[i - 1][j] == 0

    def ONTABLE(self, X):
        pos = self.find_box(X)
        return pos and pos[0] == 3

    def FREE(self):
        if self.holding == 0:
            return True
        i, j = self.position
        item = self.grid[i][j]
        if item == 0:
            self.PLACEONTABLE(item)
        self.PLACE_ON(item)
        #dropped_item = self.holding
        self.log_action(f"FREE() releases to {item}")
        self.holding = 0
        return False

    def READY(self):
        self.ready = True
        self.log_action("READY()")
        return self.ready

    def GRASPING(self, X):
        if self.holding == X:
            return True
        result = self.GRASP(X)
        return self.holding == X

    def ON(self, X, Y):
        x_pos = self.find_box(X)
        y_pos = self.find_box(Y)
        return x_pos and y_pos and x_pos[0] == y_pos[0] - 1 and x_pos[1] == y_pos[1]

    def ONLEFT(self, X, Y):
        x_pos = self.find_box(X)
        y_pos = self.find_box(Y)
        return x_pos and y_pos and x_pos[0] == y_pos[0] and x_pos[1] == y_pos[1] - 1

    def ONRIGHT(self, X, Y):
        x_pos = self.find_box(X)
        y_pos = self.find_box(Y)
        return x_pos and y_pos and x_pos[0] == y_pos[0] and x_pos[1] == y_pos[1] + 1

    def UNDER(self, X, Y):
        return self.ON(Y, X)

    def MOVETO(self, X):
        self.log_action(f"MOVETO({X})")
        self.position = self.find_box(X)
        return self.position

    def MOVELEFT(self):
        x_pos, y_pos = self.position
        self.position = (x_pos, y_pos-1)
        self.log_action("MOVELEFT()")

    def MOVERIGHT(self):
        x_pos, y_pos = self.position
        self.position = (x_pos, y_pos+1)
        self.log_action("MOVERIGHT()")
        
    def PLACE_ON(self, target_box):
        if not self.holding:
            print("Nothing to place")
            return
        pos = self.find_box(target_box)
        if not pos:
            print(f"{target_box} not found")
            return
        i, j = pos
        if i == 0:
            print(f"Cannot place on {target_box} (top row)")
            return
        if self.grid[i - 1][j] == 0:
            self.grid[i - 1][j] = self.holding
            print(f"Placed {self.holding} on {target_box} at ({i - 1}, {j})")
            self.holding = 0
        else:
            print(f"Space above {target_box} is occupied")

    def PLACEONTABLE(self, X):
        if self.holding != X:
            return
        i, j = self.position
        self.grid[i][j] = self.holding
        self.log_action(f"PLACEONTABLE({self.holding}) at ({i}, {j})")
        self.holding = 0
        return


    def GRASP(self, X):
        if self.holding:
            return False
        pos = self.find_box(X)
        if pos and self.CLEAR(X):
            i, j = pos
            self.grid[i][j] = 0
            self.holding = X
            self.log_action(f"GRASP({X}) from ({i}, {j})")
            return True
        return False

    def NOP(self):
        self.READY()
        self.log_action("NOP()")

    def find_box(self, box):
        for i in range(4):
            for j in range(4):
                if self.grid[i][j] == box:
                    return (i, j)
        return None

    def print_state(self):
        for row in self.grid:
            print(['0' if x == 0 else x for x in row])
        print("Holding:", self.holding if self.holding else "None")
        print("____________________________________________")
        print("\n")
        
    def print_log(self):
        print("\nExecuted Steps:")
        for step in self.log:
            print(step)

    def reset(self):
        self.__init__()

# ================= TASKS (Formal Redefinition) ===================

robot = RobotArm4x4()

print("\nFormal Language Expression: State So")
print(" using matrix (y, x) from (0, 0) to (3,3) ")
robot.READY()
robot.log_action("ONTABLE(A), ONTABLE(B), ONTABLE(C), ONTABLE(D)")
robot.log_action("ONLEFT(A,B), ONLEFT(B,C), ONLEFT(C,D)")
robot.FREE()
robot.print_log()
print("\n")
robot.print_state()
robot.reset()

# Task 1: Swap B and C
print("\nTask 1: Swapping B and C")
robot.READY()
robot.MOVETO("B")
robot.GRASP("B")
robot.MOVETO("A")
robot.FREE()
robot.MOVETO("C")
robot.GRASP("C")
robot.MOVELEFT()
robot.PLACEONTABLE("C")
robot.MOVETO("B")
robot.GRASP("B")
robot.MOVETO("C")
robot.MOVERIGHT()
robot.PLACEONTABLE("B")
robot.FREE()
robot.print_log()
print("\n")
robot.print_state()
robot.reset()

# Task 2: Place B under A
print("\nTask 2: Placing B under A")
robot.READY()
robot.MOVETO("A")
robot.GRASP("A")
robot.MOVETO("C")
robot.FREE()
robot.MOVETO("B")
robot.GRASP("B")
robot.MOVELEFT()
robot.PLACEONTABLE("B")
robot.MOVETO("A")
robot.GRASP("A")
robot.MOVETO("B")
robot.FREE()
robot.print_log()
print("\n")
robot.print_state()
robot.reset()

# Task 3: Place D on top of B
print("\nTask 3: Placing D on top of B")
robot.READY()
robot.MOVETO("D")
robot.GRASP("D")
robot.MOVETO("B")
robot.FREE()
robot.print_log()
print("\n")
robot.print_state()
robot.reset()


# Task 4: Stack A-B-C-D (A at bottom)
print("\nTask 4: Stack A-B-C-D")
robot.READY()
robot.MOVETO("B")
robot.GRASP("B")
robot.MOVETO("A")
robot.FREE()
robot.MOVETO("C")
robot.GRASP("C")
robot.MOVETO("B")
robot.FREE()
robot.MOVETO("D")
robot.GRASP("D")
robot.MOVETO("C")
robot.FREE()
robot.print_log()
print("\n")
robot.print_state()
robot.reset()

# Task 5: Stack D-C-B-A (D at bottom)
print("\nTask 5: Stack D-C-B-A")
robot.READY()
robot.MOVETO("C")
robot.GRASP("C")
robot.MOVETO("D")
robot.FREE()
robot.MOVETO("B")
robot.GRASP("B")
robot.MOVETO("C")
robot.FREE()
robot.MOVETO("A")
robot.GRASP("A")
robot.MOVETO("B")
robot.FREE()
robot.print_log()
print("\n")
robot.print_state()