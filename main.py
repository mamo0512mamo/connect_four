import pygame
from settings import SCREEN_HEIGHT, SCREEN_WIDTH
from player import ManualPlayer, RandomPlayer, DQNPlayer
from datetime import datetime
from game import Game

def reset_game_state(game):
    game.reset_game()
    return 1, 0, False


def main():
    # player_1 = DQNPlayer(1, do_learn=True)
    # player_2 = DQNPlayer(2, do_learn=True)

    # player_1 = DQNPlayer(1, do_learn=False)
    # player_2 = ManualPlayer(2)
    # player_1.load("/Users/mamorukariya/Desktop/pygame/connect_four/models/model2_0_2025-08-01 18:07:03.476306.pth")

    player_1 = ManualPlayer(1)
    player_2 = DQNPlayer(2, do_learn=False)
    player_2.load("/Users/mamorukariya/Desktop/pygame/connect_four/models/model2_1_2025-08-01 18:13:57.133624.pth")


    players = [None, player_1, player_2]
    game_count = 0
    win_count = [0, 0, 0, 0]
    win_count_100 = [0, 0, 0, 0]
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    sum_of_loss1 = 0
    sum_of_loss2 = 0
    while True:
        game = Game(players)
        game.init_display(screen, clock) #
        winner, loss1, loss2 = game.play()
        if loss1 != None:
            sum_of_loss1 += loss1
        if loss2 != None:
            sum_of_loss2 += loss2
        game_count += 1
        win_count[winner] += 1
        win_count_100[winner] += 1
        if (game_count % 100) == 0:
            print(game_count ,*win_count_100[1:])
            win_count_100 = [0, 0, 0, 0]
            print(sum_of_loss1 / 100, sum_of_loss2 / 100)
            sum_of_loss1 = 0
            sum_of_loss2 = 0
        if (game_count + 1) % 10000 == 0:
            players[1].save(f'models/model1_{game_count//10000}_{datetime.now()}.pth')
            players[2].save(f'models/model2_{game_count//10000}_{datetime.now()}.pth')
            print('saved')
            
            
if __name__ == '__main__':
    main()


#time sleep
