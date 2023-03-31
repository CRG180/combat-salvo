from hetrogenous_salvo_read_data import read_input_file
import numpy as np


class Unit:
    def __init__(self,unit_dict):
        self.formation = unit_dict["formation"]
        self.type = unit_dict["type"]
        self.mgrs = unit_dict["mgrs"]
        self.range = unit_dict["range"]
        self.num_units = unit_dict["num_units"]
        self.num_missiles_off = unit_dict["num_missiles_off"]
        self.num_missiles_def = unit_dict["num_missiles_def"]
        self.aimed_offense  = unit_dict["aimed_offense"]
        self.fraction_engage = unit_dict["fraction_engage"]
        self.defense_capability = unit_dict["defense_capability "]
        self.staying_power = unit_dict["staying_power"]
        self.scouting = unit_dict["scouting"]
        self.alertness = unit_dict["alertness"]
        self.training = unit_dict["training"]
        self.distraction = unit_dict["distraction"]
    
    @property
    def offense_shots_available(self):
        return self.num_units * self.num_missiles_off
        
    @property
    def defense_shots_available(self):
        return self.num_units * self.num_missiles_def
    
    def update_num_off_missiles(self):
        pass
    
    def update_num_def_missiles(self):
        pass
    
    @property
    def offense_vector(self): # need off potential check, if enemy aspect hear add arg
        _matrix = np.concatenate((self.scouting, \
		self.training,self.distraction,self.fraction_engage),\
		axis = 0)	
        return _matrix.sum(axis=0)
    
    def __repr__(self) -> str:
        return f"{self.formation}"
    
    def __str__(self) -> str:
    	return f"{self.formation} {self.type} {self.num_units}x Units \
--- Total Offense Muntions {self.offense_shots_available} \
--- Total Defense Munitions {self.defense_shots_available} "
    
class BattleGroup:
    def __init__(self,unit_dict, battle_group_name = "blue"):
        self.units = []
        self.battle_group_name = battle_group_name
        for i in unit_dict:
            self.units.append(Unit(i))
    
    @property
    def num_formation(self) -> float:
        return len(self.units)
    
    @property
    def offense_matrix(self):
        pass
            
    def __str__(self) -> str:
        return f"{self.units}"

class Engagement:
    def __init__(self,blue_force, red_force, offensive_side = "blue_force"):
        self.blue_force = blue_force 
        self.red_fores = red_force
        self.offensive_side = offensive_side
        
    def build_offense_matrix(self):
        
        if self.offensive_side == "blue_force":
            off_matrix = np.zeros(len(self.blue_force.num_formations), len(self.red_fores.num_formations))
			
			
        else:
            pass
            
        return off_matrix
    
    def build_defense_matrix(self):
        pass
    
    def decrement_attrition_values(self):
        pass
    
    def salvo_engagment(self):
        pass
    
if __name__ == "__main__":
    data = read_input_file()
    b = BattleGroup(data)
    print(b)
    