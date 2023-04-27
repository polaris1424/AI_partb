# COMP30024 Artificial Intelligence, Semester 1 2023
# Project Part B: Game Playing Agent
from math import log
from random import random
from typing import Optional
from agent.state import State
from agent.node import Node
from math import sqrt
from referee.game import \
    PlayerColor, Action, SpawnAction, SpreadAction, HexPos, HexDir


# This is the entry point for your game playing agent. Currently the agent
# simply spawns a token at the centre of the board if playing as RED, and
# spreads a token at the centre of the board if playing as BLUE. This is
# intended to serve as an example of how to use the referee API -- obviously
# this is not a valid strategy for actually playing the game!
 


class Agent:
    def __init__(self, color: PlayerColor, **referee: dict):
        """
        Initialise the agent.
        """
        self._color = color
        match color:
            case PlayerColor.RED:
                print("Testing: I am playing as red")
            case PlayerColor.BLUE:
                print("Testing: I am playing as blue")
        self.root = Node()

     
    
    def action(self, **referee: dict) -> Action:
        #using  Monte Carlo Tree Search (MCTS) to find the best action
        #return the best action
        num_iterations = 100
        while(num_iterations):
            #selection
            selected_node = self.selection(self.root)
            if selected_node is None:
                break
            #expansion
            expanded_ndoe = self.expansion(selected_node)
            if expanded_ndoe is None:
                break
            #simulation
            reward = self.simulation(expanded_ndoe)
            #backpropagation回溯，更新整个模拟的游戏，谁赢+1，谁输-1
            self.backpropagation(expanded_ndoe, reward)
            
            num_iterations -= 1
        #return the best action
        return self.root.get_best_action()
                

    def selection(self, node: Node)-> Optional[Node]:
        # select a node to expand based on the UCB1 formula
        if node.is_terminal():
            # 如果是终止节点，直接返回 None
            return None
        """节点A有三个子节点,其中节点1和节点2已被访问和拓展,但是节点3还未被访问和拓展。
        因此,节点A尚未被完全扩展,我们需要选择一个未扩展的子节点进行扩展,返回节点A。   
        """
        """如果节点A的每个子节点都已经被访问和拓展,那么在执行MCTS的selection步骤时,
        会选择具有最高UCB1值的子节点进行拓展。因此,如果在这种情况下执行selection,
        它应该返回具有最高UCB1值的子节点。
        """

        if not node.is_fully_expanded():
            return node
        else:
            c = 1
            # 选择具有最高UCB1值的子节点进行拓展
            best_child = node.get_best_child(c)
            return  best_child
         
 
    def expansion(self, node: Node, action: Action)->Node:
        # expand the selected node by adding a new child node  

        if node.is_terminal():
            # 如果是终止节点，直接返回 None
            return None
        if node.is_fully_expanded():
            # 如果所有动作都已经扩展，直接返回 None
            return None
        else:
            # 选择一个未扩展的动作进行扩展
            actions = node.get_untried_actions() #修改？？
            action = random.choice(actions)
            new_node = node.expand(action)

            return new_node

    def simulation(self, node: Node)->int:
        #"修改！！！！！！！！！！！！！！！！！！！！！！！！！！！
        # 模拟"阶段（simulation phase）。在该算法中，从上一步得到的节点开始，随机地选择动作，
        # 直到模拟到达游戏的终止状态。在这里，我们假设模拟到达游戏的终止状态后，能得到该局的回报。
        # 该回报将作为"回溯"阶段的输入。
        #return reward
        state  = node.get_state()
        while not state.is_terminal():
            #需要修改，随机选择动作，随机选择，既可以spread 又可以spaw
            legal_actions = state.get_legal_actions()  # 获得当前合法的动作n

            action = random.choice(legal_actions)
            state = state.get_next_state(action)
        
        reward = state.get_reward(self._color)
        return reward


    def backpropagation(self, node: Node, reward: int):
        #backpropagation phase
        #update the node's win and visit count
        #update the node's parent's win and visit count
        #update the node's parent's parent's win and visit count
        #从当前节点开始，沿着父节点往上回溯，更新每个节点的 visit 和 reward
        node.visits += 1
        node.wins += reward
        if node.parent is not None:
            self.backpropagation(node.parent, reward)
        else:
            return None



    def action(self, **referee: dict) -> Action:
        """
        Return the next action to take.
        """
        match self._color:
            case PlayerColor.RED:
                return SpawnAction(HexPos(3, 3))
            case PlayerColor.BLUE:
                # This is going to be invalid... BLUE never spawned!
                return SpreadAction(HexPos(3, 3), HexDir.Up) 
                
    
    def turn(self, color: PlayerColor, action: Action, **referee: dict):
        """
        Update the agent with the last player's action.
        """
        match action:
            case SpawnAction(cell):
                print(f"Testing: {color} SPAWN at {cell}")
                pass
            case SpreadAction(cell, direction):
                print(f"Testing: {color} SPREAD from {cell}, {direction}")
                pass
