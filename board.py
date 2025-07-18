import pygame
from settings import DARK_RED, BLUE, DARK_GRAY, BLACK
class Board:
    def __init__(self):
        self.state = [[0 for _ in range(7)] for _ in range(6)]
        self.game_over = False

        
    def make_move(self, column, player):#specify which board to change
        if self.game_over:
            return False
        if not column == None:
            for row in range(5, -1, -1): 
                if self.state[row][column] == 0:  
                    self.state[row][column] = player
                    return True
        return False
    
    @classmethod
    def make_move_class(cls, state, column, player):
        if not column == None:
            for row in range(5, -1, -1): 
                if state[row][column] == 0:  
                    state[row][column] = player
                    return True
        return False


    def check_win(self):
        for row in range(6):
            for col in range(4):
                if self.state[row][col] == self.state[row][col+1] == self.state[row][col+2] == self.state[row][col+3] != 0:
                    if self.state[row][col] == 1:
                        return 1
                    else:
                        return 2
        for row in range(3):
            for col in range(7):
                if self.state[row][col] == self.state[row+1][col] == self.state[row+2][col] == self.state[row+3][col] != 0:
                    if self.state[row][col] == 1:
                        return 1
                    else:
                        return 2
        for row in range(3, 6):
            for col in range(4):
                if self.state[row][col] == self.state[row-1][col+1] == self.state[row-2][col+2] == self.state[row-3][col+3] != 0:
                    if self.state[row][col] == 1:
                        return 1
                    else:
                        return 2
        for row in range(3):
            for col in range(4):
                if self.state[row][col] == self.state[row+1][col+1] == self.state[row+2][col+2] == self.state[row+3][col+3] != 0:
                    if self.state[row][col] == 1:
                        return 1
                    else:
                        return 2
        if len(self.valid_moves()) == 0:
            return 3
        return 0
    
    def check_game_over(self):
        winner = self.check_win()
        if winner != 0:
            return winner, True
        return 0, False
    
    def valid_moves(self):
        valid = []
        for i in range(7):
            if self.state[0][i] == 0:
                valid.append(i + 1)
        return valid
        

    def draw_board(self, screen):
        screen.fill(BLACK)
        for row in range(6):
            for col in range(7):
                if self.state[row][col] == 0:
                    color = DARK_GRAY
                elif self.state[row][col] == 1:
                    color = DARK_RED
                else:
                    color = BLUE
                pygame.draw.circle(screen, color, (col * 100 + 50, row * 100 + 50), 40)
    
    def reset_game(self):
        self.state = [[0 for _ in range(7)] for _ in range(6)]
        self.game_over = False
