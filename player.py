import random
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from collections import deque
import pygame 
from board import Board
import copy


class Player:
    def __init__(self, player_number):
        self.player_number = player_number

    def valid_moves(self, state):
        valid = []
        for i in range(7):
            if state[0][i] == 0:
                valid.append(i)
        return valid
    
    def remember(self, past_state, past_selected_column, reward_pastplayer, current_state, done):
        pass

    def replay(self):
        pass

    def save(self, filepath):
        pass

    def choose_move(self, state):
        pass



class ManualPlayer(Player):

    def handle_human_player_input(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x_pos = event.pos[0]
                    selected_column = x_pos // 100
                    return selected_column
    
    def choose_move(self, state):
        while True:
            move = self.handle_human_player_input()
            if move in self.valid_moves(state):
                return move
    
class RandomPlayer(Player):
    def choose_move(self, state):
        valid = self.valid_moves(state)
        return valid[random.randrange(len(valid))]
    

class DQNPlayer(Player):
    def __init__(self, is_first_player, do_learn=True):
        super().__init__(is_first_player)

        self.action_size = 7
        
        # Hyperparameters
        self.hidden_size = 128
        self.learning_rate = 0.01#
        self.gamma = 0.80#
        self.epsilon = 1
        self.epsilon_decay = 0.9998#
        self.batch_size = 64
        self.memory_size = 10000
        self.epsilon_min = 0.3#
        self.do_learn = do_learn

        if not do_learn:
            self.epsilon = 0
            self.epsilon_min = 0
            self.learning_rate = 0

        
        self.memory = deque(maxlen = self.memory_size)

        self.q_network = self._build_model()
        self.target_network = self._build_model()
        self.update_target_network()
        
        self.optimizer = optim.Adam(self.q_network.parameters(), lr=self.learning_rate)
    
    def _build_model(self):
        return nn.Sequential(
            nn.Conv2d(1, 32, kernel_size=3, padding=1),  # Convolutional layer
            nn.ReLU(),
            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.Flatten(),  # Flatten the 2D grid
            nn.Linear(64 * 6 * 7, self.hidden_size),  # Fully connected layer
            nn.ReLU(),
            nn.Linear(self.hidden_size, self.action_size)  # Output layer
        )


    def update_target_network(self):
        self.target_network.load_state_dict(self.q_network.state_dict())
    
    def remember(self, past_state, past_selected_column, reward, next_state, done):
        if self.do_learn == False:
            return
        self.memory.append((past_state, past_selected_column, reward, next_state, done))
    
    def choose_move(self, state):
        valid = self.valid_moves(state)
        if np.random.rand() <= self.epsilon:
            return valid[random.randrange(len(valid))]
        else:
            state_tensor = torch.FloatTensor(state)
            state_tensor = state_tensor.view(-1, 1, 6, 7)#view(-1)
            q_values = self.q_network(state_tensor)
            maxi = None
            maxv = -10000000000000
            for i in range(7):
                if i in valid and q_values[0][i].item() > maxv:
                    maxv = q_values[0][i].item()
                    maxi = i    
            return maxi
    
    def maxq_from_nextqvalues(self, next_states):
        list_max_v = []
        for state in next_states:
            state = state[0]
            valid = self.valid_moves(state)
            state_tensor = torch.FloatTensor(state)
            state_tensor = state_tensor.view(-1, 1, 6, 7)
            q_values = self.q_network(state_tensor)
            maxv = -10000000000000
            for i in range(7):
                if i in valid:
                    if q_values[0][i].item() > maxv:
                        maxv = q_values[0][i].item()
            list_max_v.append(maxv)
        return torch.tensor(list_max_v) 
        
    
    def replay(self):
        if len(self.memory) < self.batch_size:
            return
        
        if self.do_learn == False:
            return
        batch = random.sample(self.memory, self.batch_size)
        past_states, past_selected_columns, rewards, next_states, dones = zip(*batch)
        


        past_states = [torch.tensor(state) for state in past_states]
        next_states = [torch.tensor(state) for state in next_states]
        past_selected_columns = torch.tensor(past_selected_columns)
        rewards = torch.tensor(rewards)
        past_states = torch.stack(past_states)
        past_states = past_states.float()
        past_states = past_states.view(-1, 1, 6, 7)
        next_states = torch.stack(next_states)
        next_states = next_states.float()
        next_states = next_states.view(-1, 1, 6, 7)
        dones = torch.tensor(dones)
        dones = dones.float()
        
        next_q_values = self.maxq_from_nextqvalues(next_states) # Take max Q-value across actions
        target_q_values = rewards + (1 - dones) * self.gamma * next_q_values
        past_selected_columns = torch.clamp(past_selected_columns, min=0, max=6)
        q_values = self.q_network(past_states).gather(1, past_selected_columns.unsqueeze(1)).squeeze(1)
        
        loss = nn.MSELoss()(q_values, target_q_values)
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
        self.update_target_network()

        self.epsilon *= self.epsilon_decay
        if self.epsilon < self.epsilon_min:
            self.epsilon = self.epsilon_min
        
    
    def save(self, filepath):
        torch.save(self.q_network.state_dict(), filepath)
    
    def load(self, filepath):
        self.q_network.load_state_dict(torch.load(filepath))
        self.update_target_network()

