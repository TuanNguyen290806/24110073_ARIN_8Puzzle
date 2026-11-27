from itertools import count
import heapq

class Node:
    def __init__(self, state, parent=None, action=None, path_cost=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost

class PriorityQueue:
    def __init__(self):
        self.heap = []
        self.nodes={}
        self.counter=count()  

    def enqueue(self, node):
        self.nodes[node.state]=node
        heapq.heappush(self.heap, (node.path_cost, next(self.counter), node))

    def dequeue(self):
        while True:
            _, _, node = heapq.heappop(self.heap)
            if self.nodes.get(node.state) is node:
                del self.nodes[node.state]
                return node

    def is_empty(self):
        return len(self.nodes) == 0

    def __contains__(self, node):
        return node.state in self.nodes

    def cost_of(self,node):
        return self.nodes[node.state].path_cost
    
    def replace(self,node):
        self.enqueue(node)

def child_node(problem, node, action):
    child_state = problem.result(node.state, action)
    cost = node.path_cost + problem.step_cost(node.state, action)
    return Node(child_state, parent=node, action=action, path_cost=cost)

def solution(node):
    actions = []
    while node.parent is not None:
        actions.append(node.action)
        node = node.parent
    actions.reverse()
    return actions

def UCS(problem):
    node = Node(problem.initial_state,path_cost=0)
    frontier = PriorityQueue()
    frontier.enqueue(node)
    explored = set()
    while not frontier.is_empty():
        node = frontier.dequeue()
        if problem.is_goal(node.state):
            return solution(node)
        explored.add(node.state)

        for action in problem.actions(node.state):
            child = child_node(problem, node, action)
            if child.state not in explored and child not in frontier:
                frontier.enqueue(child)
            elif child in frontier and child.path_cost < frontier.cost_of(child):
                frontier.replace(child)
    return None

class EightPuzzle:
    GOAL = (1, 2, 3, 4, 5, 6, 7, 8, 0)
    COSTS = {"Up":1,"Down":1,"Left": 2, "Right": 2}
    def __init__(self, initial):
        self.initial_state = tuple(initial)

    def is_goal(self, state):
        return state == self.GOAL

    def actions(self, state):
        row, col = divmod(state.index(0), 3)
        acts = []
        if row > 0: acts.append("Up")
        if row < 2: acts.append("Down")
        if col > 0: acts.append("Left")
        if col < 2: acts.append("Right")
        return acts
    def result(self, state, action):
        i = state.index(0)
        j = i + {"Up": -3, "Down": 3, "Left": -1, "Right": 1}[action]
        s = list(state)
        s[i], s[j] = s[j], s[i]
        return tuple(s)

    def step_cost(self, state, action):
        return self.COSTS[action]

def main():
    tiles = tuple(map(int, input("Enter 9 tiles: ").split()))
    problem = EightPuzzle(tiles)
    result = UCS(problem)
    if sorted(tiles) != list(range(9)):
        print("Invalid input: every digit from 0 to 8 appears only ONCE.")
        return
    if result is None:
        print("Unsolvable.")
    else:
        print("Result:", result)
        print("Steps:", len(result))
        cost = sum(problem.step_cost(None, a) for a in result)
        print("Total cost:", cost)
if __name__ == "__main__":
    main()

"""
class VacuumWorld:
    COSTS = {"Left": 1, "Right": 1, "Suck": 2}
    def __init__(self, location, dirt_a, dirt_b):
        self.initial_state = (location, dirt_a, dirt_b)
    def is_goal(self, state):
        loc,a,b = state
        return not a and not b
    def actions(self, state):
        loc,a,b = state
        acts=[]
        if loc=='B': acts.append("Left")
        if loc== 'A': acts.append("Right")
        if (loc=='A' and a) or (loc == 'B' and b):
            acts.append("Suck")
        return acts
    def result(self, state, action):
        loc,a,b = state
        if action=="Left": return ('A',a,b)
        if action=="Right": return ('B',a,b)
        if action=="Suck1":
            return (loc,False,b) if loc == 'A' else (loc,a,False)
    def step_cost(self, state, action):
        return self.COSTS[action]

def main():
    loc = input("Initial room (A/B): ").strip().upper()
    a = input("Is room A dirty? (1=Yes, 0=No): ").strip() == "1"
    b = input("Is room B dirty? (1=Yes, 0=No): ").strip() == "1"
    if loc not in ("A", "B"):
        print("Invalid input: must be A or b.")
        return
    problem = VacuumWorld(loc, a, b)
    result = UCS(problem)
    print(result, "Steps:", len(result) if result is not None else "Unsolvable")

if __name__ == "__main__":
    main()
"""

               