'''
Lab 13: My first AI agent.
In this lab, you will create your first AI agent.
You will use the run_episode function from lab 12 to run a number of episodes
and collect the returns for each state-action pair.
Then you will use the returns to calculate the action values for each state-action pair.
Finally, you will use the action values to calculate the optimal policy.
You will then test the optimal policy to see how well it performs.

Sidebar-
If you reward every action you may end up in a situation where the agent
will always choose the action that gives the highest reward. Ironically,
this may lead to the agent losing the game.
'''
import sys
from pathlib import Path

# line taken from turn_combat.py
sys.path.append(str((Path(__file__) / ".." / "..").resolve().absolute()))

from lab11.pygame_combat import PyGameComputerCombatPlayer
from lab11.turn_combat import CombatPlayer
from lab12.episode import run_episode

from collections import defaultdict
import random
import numpy as np


class PyGameRandomCombatPlayer(PyGameComputerCombatPlayer):
    def __init__(self, name):
        super().__init__(name)

    def weapon_selecting_strategy(self):
        self.weapon = random.randint(0, 2)
        return self.weapon


class PyGamePolicyCombatPlayer(CombatPlayer):
    def __init__(self, name, policy):
        super().__init__(name)
        self.policy = policy

    def weapon_selecting_strategy(self):
        self.weapon = self.policy[self.current_env_state]
        return self.weapon


def run_random_episode(player, opponent):
    player.health = random.choice(range(100, 110, 10))
    opponent.health = random.choice(range(100, 110, 10))
    return run_episode(player, opponent)


def get_history_returns(history):
    total_return = sum([reward for _, _, reward in history])
    returns = {}
    for i, (state, action, reward) in enumerate(history):
        if state not in returns:
            returns[state] = {}
        returns[state][action] = total_return - sum(
            [reward for _, _, reward in history[:i]]
        )
    return returns



def run_episodes(n_episodes):

    #initialization
    reward={}
    
    action_values = defaultdict(lambda: defaultdict(float))
    Player1 = PyGameRandomCombatPlayer("Player1")
    Player2 = PyGameComputerCombatPlayer("Player2")

    #iterates the episodes
    for i in range(n_episodes):
        #runs an episode, saves it as a history return
        someRandomList = run_random_episode(Player1, Player2)
        returns = get_history_returns(someRandomList)
        for state,actions in returns.items():
            if state not in reward:
                reward[state]={}
            for action,rewards in actions.items():
                if action not in reward[state]:
                    reward[state][action]=[]
                reward[state][action].append(rewards)

    #averaging
    for state,action in reward.items():
        if state not in action_values:
            action_values[state]={}
        for actiondict,rewards in action.items():        
            action_values[state][actiondict]=sum(rewards)/len(rewards)

    #hard value
    action_values[(100,100)][1]=1
    return action_values


def get_optimal_policy(action_values):
    optimal_policy = defaultdict(int)
    for state in action_values:
        optimal_policy[state] = max(action_values[state], key=action_values[state].get)
    return optimal_policy


def test_policy(policy):
    names = ["Legolas", "Saruman"]
    total_reward = 0
    for _ in range(100):
        player1 = PyGamePolicyCombatPlayer(names[0], policy)
        player2 = PyGameComputerCombatPlayer(names[1])
        players = [player1, player2]
        total_reward += sum(
            [reward for _, _, reward in run_episode(*players)]
        )
    return total_reward / 100


if __name__ == "__main__":
    action_values = run_episodes(10)
    print(action_values)
    optimal_policy = get_optimal_policy(action_values)
    print("\n\n")
    print(optimal_policy)
    #print(test_policy(optimal_policy))
