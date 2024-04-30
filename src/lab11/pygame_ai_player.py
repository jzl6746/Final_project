""" Create PyGameAIPlayer class here"""
import pygame
import time
from lab11.turn_combat import CombatPlayer
#from lab13.rl_episodes import get_optimal_policy, run_episodes####
import random
#movement
#hardcode city traversal routes dont matter
#end at city 9
class PyGameAIPlayer:
    def __init__(self) -> None:
        pass

    def selectAction(self, state):  
        time.sleep(0.0000000000001)
        next=state.current_city
        print(next)
        while not state.travelling:
            next=next+1  
            return ord(str(next%10))

""" Create PyGameAICombatPlayer class here"""

#combat
class PyGameAICombatPlayer(CombatPlayer):
    def __init__(self, name):
        super().__init__(name)

    def weapon_selecting_strategy(self):

        #optimal =get_optimal_policy(run_episodes(1000))
        #P1=PyGameAICombatPlayer("AI")
        #P2=CombatPlayer("Comp")
    


        while True:
            #for i in range(optimal):
                #if optimal[i][0]==(P1.health,P2.health):
                    #return optimal[i][1]
                #else:
                    return random.randint(0,2)
            





            
