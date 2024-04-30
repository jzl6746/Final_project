''' 
Lab 12: Beginnings of Reinforcement Learning

Create a function called run_episode that takes in two players
and runs a single episode of combat between them. 
As per RL conventions, the function should return a list of tuples
of the form (observation/state, action, reward) for each turn in the episode.
Note that observation/state is a tuple of the form (player1_health, player2_health).
Action is simply the weapon selected by the player.
Reward is the reward for the player for that turn.
'''
import sys
from pathlib import Path
sys.path.append(str((Path(__file__) / ".." / "..").resolve().absolute()))
from lab11.turn_combat import CombatPlayer,Combat
from lab11.pygame_combat import PyGameComputerCombatPlayer,draw_combat_on_window,run_turn
from lab11.pygame_ai_player import PyGameAICombatPlayer






Player1 = PyGameAICombatPlayer("Player1")
Player2 = PyGameComputerCombatPlayer("Player2")
def run_episode(Player1,Player2):
    currentGame = Combat()
    my_list=[]
    

    while not currentGame.gameOver:
        reward = run_turn(currentGame, Player1, Player2)
        my_list.append(((Player1.health,Player2.health), Player1.weapon, reward))

    
    return my_list
    

run_episode(Player1,Player2)
    

    




    