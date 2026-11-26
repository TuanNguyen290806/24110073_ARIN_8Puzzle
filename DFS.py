class Node:
   def __init__(self,state, parent=None, action=None):
    self.state=state
    self.parent=parent
    self.action=action

class Stack:
    def __init__(self):
        self.items=[]
        self.states=set()
    def push(self,node):
       self.items.append(node)
       self.states.add(node.state)
    def pop(self):
       node=self.items.pop()
       self.states.discard(node.state)
       return node
    def is_empty(self):
       return len(self.items)==0
    def __contains__(self,node):
       return node.state in self.states

def child_node(problem, node, action):
    child_state = problem.result(node.state, action)
    return Node(child_state, parent=node, action=action)

def solution(node):
    actions = []
    while node.parent is not None:
        actions.append(node.action)
        node = node.parent
    actions.reverse()
    return actions

def DFS(problem):
   node=Node(problem.initial_state)
   if problem.is_goal(node.state):
      return solution(node)
   frontier=Stack()
   frontier.push(node)
   explored=set()
   while not frontier.is_empty():
      node=frontier.pop()
      explored.add(node.state)

      for action in problem.actions(node.state):
         child=child_node(problem,node,action)
         if child.state not in explored and child not in frontier:
            if problem.is_goal(child.state):
               return solution(child)
            frontier.push(child)
   return None

class EightPuzzle:
    GOAL = (1, 2, 3, 4, 5, 6, 7, 8, 0)

    def __init__(self, initial):
        self.initial_state = tuple(initial)

    def is_goal(self, state):
        return state == self.GOAL

    def actions(self, state):
        row, col = divmod(state.index(0), 3)
        acts = []
        if row > 0: acts.append("Len")
        if row < 2: acts.append("Xuong")
        if col > 0: acts.append("Trai")
        if col < 2: acts.append("Phai")
        return acts
    def result(self, state, action):
        i = state.index(0)
        j = i + {"Len": -3, "Xuong": 3, "Trai": -1, "Phai": 1}[action]
        s = list(state)
        s[i], s[j] = s[j], s[i]
        return tuple(s)

def main():
    tiles = tuple(map(int, input("Nhap 9 o: ").split()))
    if sorted(tiles) != list(range(9)):
        print("Nhap sai: moi so tu 0 den 8 xuat hien dung 1 lan.")
        return
    problem = EightPuzzle(tiles)
    result = DFS(problem)
    if result is None:
        print("Khong giai duoc.")
    else:
        print("Dap an:", result)
        print("So buoc di:", len(result))

if __name__ == "__main__":
    main()
               
      

