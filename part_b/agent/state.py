from typing import List, Tuple
from referee.game.actions import Action

from referee.game.player import PlayerColor
from referee.game.hex import HexPos


class State:
    def init(self, board: List[List[int]], color: PlayerColor):
        self.board = board
        self.color = color
 

    def is_terminal(self) -> bool:
        """
        判断当前状态是否为终止状态，即有一方获胜或者平局。
        """
        # 判断是否有一方获胜，此处略去具体实现
        if self.has_winner():
            return True
        # 判断是否平局，即是否所有格子都已经落子
        for row in self.board:
            for cell in row:
                if cell == 0:
                    return False
        return True

 
    def get_legal_actions(self) -> Action:  # List[HexPos] 
        #修改，使其可以返回所有可能的下一步动作，例如：SpawnAction(HexPos(3, 3)) SpreadAction(HexPos(3, 3), HexDir.Up)
        
        # 该函数返回当前状态下所有合法的动作
        """legal_actions = []
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] == 0:
                    legal_actions.append(HexPos(i, j))
        return legal_actions """
        
 
    

    def get_next_state(self, action: Tuple[int, int]) -> 'State':
        """
        执行给定动作，返回新状态。
        """
        i, j = action
        next_board = [row.copy() for row in self.board]  # 复制棋盘
        next_board[i][j] = self._color  # 落子
        next_color = PlayerColor.RED if self._color == PlayerColor.BLUE else PlayerColor.BLUE  # 切换玩家
        return State(next_board, next_color)
 
   
    def get_reward(self, player: PlayerColor) -> float:
        """
        返回给定玩家在当前状态下的奖励。
        """
        if self.has_winner() and self.winner == player:
            return 1.0  # 获胜
        elif self.has_winner() and self.winner != player:
            return -1.0 # 失败
        else:
            return 0.0 # 平局或者未结束
 
