#!/usr/bin/env python3
from battleGroup import BattleGroup
import numpy as np


class Engagement:
    
    def __init__(self,blue_force:BattleGroup, red_force:BattleGroup, offensive_side = "blue_force"):
        self.blue_force = blue_force 
        self.red_force = red_force
        self._offensive_side = offensive_side
        self.winning_side = None
        self.blue_attrited = False 
        self.red_attrited = False 
        self.iter_num = 0
    
    @property
    def battle_complete(self):
        if self.red_attrited or self.blue_attrited:
            return True
        else:
            return False
        
    def attrit_units(self, attrit_vec) ->None:
        if self._offensive_side == "blue_force":
            for unit, dec_val in zip(self.red_force.units, attrit_vec):
                unit - max(dec_val,0)
            return None
    
        if self._offensive_side == "red_force":
            for unit, dec_val in zip(self.blue_force.units, attrit_vec):
                unit - max(dec_val, 0)
            return None
        
        
    def salvo(self) -> np.array:
        
        if self._offensive_side == "blue_force":

            off = np.matmul(self.blue_force.offense_matrix,\
                self.blue_force.formation_vec)
            
            defen = np.matmul(self.red_force.defense_matrix,\
                self.red_force.formation_vec )
            
            _red_attrit_vec = (off-defen) / self.red_force.staying_power_vec

            return _red_attrit_vec

        if self._offensive_side == "red_force":
            
            off = np.matmul(self.red_force.offense_matrix,\
                self.red_force.formation_vec)
            
            defen = np.matmul(self.blue_force.defense_matrix,\
                self.blue_force.formation_vec )
            
            _blue_attrit_vec = (off-defen) / self.blue_force.staying_power_vec
            
            return _blue_attrit_vec
        
    def check_win_criteria(self):
        if sum(self.red_force.formation_vec) < 1:
            self.red_attrited = True 
        if sum(self.blue_force.formation_vec) < 1:
            self.blue_attrited = True 
        return None     
    
    def iter_salvo(self, max_iter = 20):
        for u in self.blue_force.units:
            print(u)
        for u in self.red_force.units:
            print(u)

        while self.iter_num < max_iter and not self.battle_complete:
            
            print(f"------ Salvo Iteration {self.iter_num +1 }--------")
            
            self._offensive_side = "blue_force"
            _red_attrit = self.salvo()
            
            self._offensive_side = "red_force"
            _blue_attrit = self.salvo()
            
            self._offensive_side = "blue_force"
            self.attrit_units(_red_attrit)
            
            self._offensive_side = "red_force"
            self.attrit_units(_blue_attrit)
            
            self.check_win_criteria()
            self.iter_num+=1  
            print(self.red_force)
            print(self.blue_force)
            
class SimultaneousSalvo(Engagement):
    pass

class SurpriseSalvo(Engagement):
    def iter_salvo(self):
        print("iter Salvo")
        
if __name__ == "__main__":
    pass