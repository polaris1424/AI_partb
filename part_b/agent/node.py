from math import log, sqrt
from typing import Optional

from referee.game.actions import Action


class Node:
    def __init__(self, parent=None, action=None):
        
        self.HexPos = None #HexPos(3, 3) add postion of node
        self.state = None  #当前节点的状态
        self.parent = parent
        self.action = action #从父节点到当前节点的动作
        self.children = {} #当前节点的子节点
        self.wins = 0  #当前节点的胜利次数
        self.visits = 0  #当前节点的访问次数
        #self.untried_actions = {} #当前节点的未扩展动作
        #self.player = None

    def is_leaf(self):
        #没有子节点返回True
        return len(self.children) == 0

    def get_untried_actions(self):
        #返回当前节点的未扩展动作
        tried_actions = self.children.keys()
        all_actions = self.state.get_legal_actions()
        return list(set(all_actions) - set(tried_actions))

    def is_fully_expanded(self):
        #所有动作都被扩展了返回True, 否则返回False
        return all(child in self.children for child in self.get_untried_actions())

    def is_terminal(self):
        #当前节点是否为终止节点
        return self.state.is_terminal()


    def get_best_child(self):
        # 返回当前节点的最佳子节点， use UCB1
        if self.is_leaf():
            return None
        def ucb1(child : Node):
            if child.visits == 0:
                return float("inf")
            return child.wins / child.visits + sqrt(2 * log(self.visits) / child.visits)

        return max(self.children.values(), key=ucb1)  #返回最大值的child node

    
    def expand(self, action: Action) -> 'Node':
    #Expand the node by adding a new child node for the given action.
    
        next_state = self.state.get_next_state(action)
        child = Node(state=next_state, parent=self, action=action)
        self.children[action] = child
        return child

    def get_state(self):
        return self.state

    def get_best_action(self) -> Optional[str]:
        #Return the best action
        if not self.children:
            return None
        
        best_action = None
        max_wins = float('-inf')
        
        for action, child in self.children.items():
            if child.wins > max_wins:
                best_action = action
                max_wins = child.wins
        
        return best_action

 


    



