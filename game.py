import pygame
from settings import SCREEN_HEIGHT, SCREEN_WIDTH, FPS, BLACK, LIGHT_GRAY
from player import ManualPlayer, RandomPlayer, DQNPlayer
from board import Board
import copy
import time
from datetime import datetime
import random

def reset_game_state(game):
    game.reset_game()
    return 1, 0, False


class Game:
    def __init__(self, player_list):#player_list[None, 1, 2]
        self.do_display = False
        self.game = Board()
        self.players = player_list

    def init_display(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.do_display = True

    def play(self):
        current_player = 1

        self.display()
        state_list = [copy.deepcopy(self.game.state)]
        selected_column_list = []
        while True:
            selected_column = self.players[current_player].choose_move(state_list[-1])
            selected_column_list.append(selected_column)
            self.game.make_move(selected_column, current_player)
            state_list.append(copy.deepcopy(self.game.state))
            

            self.display()

            winner, game_over = self.game.check_game_over()
            reward_currentplayer = 0
            reward_pastplayer = 0
            done = False
            if winner == current_player:
                reward_currentplayer = 1
                reward_pastplayer = -1
                done = True

            # 自分が打って相手を記憶
            # 自分が勝ったら自分も記憶
            #1手目を除く 
            #statelist[.......,c,p,c]が打ったあと
            #selected_column_list[.......,c,p,c]が打った手
            #remember(自分が打つ前、自分が打った手、その報酬、自分が打った後、勝負有無)
            if len(selected_column_list) > 1:
                self.players[3 - current_player].remember(state_list[-3], selected_column_list[-2], reward_pastplayer, state_list[-1], done)
            if done:
                self.players[current_player].remember(state_list[-2], selected_column_list[-1], reward_currentplayer, state_list[-2], True)###
                self.players[current_player].replay()
                self.players[3 - current_player].replay()
            
            if self.do_display:
                time.sleep(0.3)
                
            current_player = 3 - current_player
            
            if game_over:
                return winner


    def display(self): #private
        if self.do_display:
            self.game.draw_board(self.screen)
            pygame.display.flip()
            self.clock.tick(FPS)


