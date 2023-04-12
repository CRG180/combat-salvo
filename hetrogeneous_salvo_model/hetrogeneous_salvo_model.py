from hetrogenous_salvo_read_data import read_input_file
from dataclasses import dataclass
import numpy as np

def check_value_0_1(input_array, attribute ,formation):
    for i in input_array:
        if i > 1 or i < 0:
            raise ValueError(f"{attribute} value for {formation} is incorrect with value as {i}")
    return None
    


@dataclass
class Unit:
    unit_dict: dict
    
    @property
    def formation(self):
        return self.unit_dict["formation"]
    
    @property
    def unit_type(self):
        return self.unit_dict["type"]
    
    @property
    def mgrs(self):
        return self.unit_dict["mgrs"]
    
    @property
    def weapon_range(self):
        return self.unit_dict["range"]
    
    @property
    def num_units(self):
        return self.unit_dict["num_units"]
    
    @property
    def num_missiles_off(self):
        return self.unit_dict["num_missiles_off"]
    
    @property
    def num_missiles_def(self):
        return self.unit_dict["num_missiles_def"]
    
    @property
    def aimed_offense(self):
        return self.unit_dict["aimed_offense"]
    
    @property
    def aimed_offense(self):
        return self.unit_dict["aimed_offense"]
    
    @property
    def aimed_offense(self):
        return self.unit_dict["aimed_offense"]

    @property
    def fraction_engage(self):
        return self.unit_dict["fraction_engage"]

    @property
    def defense_capability(self):
        return self.unit_dict["defense_capability"]

    @property
    def staying_power(self):
        return self.unit_dict["staying_power"]
    
    @property
    def scouting(self):
        check_value_0_1(self.unit_dict["scouting"], "Scouting",self.formation)
        return self.unit_dict["scouting"]
    
    @property
    def alertness(self):
        return self.unit_dict["alertness"]

    @property
    def training(self):
        return self.unit_dict["training"]
    
    @property
    def distraction(self):
        return self.unit_dict["distraction"]
        
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
    def offense_vector(self) -> np.array: # check this 
        _matrix = np.concatenate(([self.scouting], \
		[self.training],[self.distraction],[self.fraction_engage]),\
		axis = 0)	
        return np.multiply.reduce(_matrix, axis=0)
    
    @property
    def defense_vector(self)-> np.array: # parameters need to be rechecked
        _matrix = np.concatenate(([self.defense_capability], \
            [self.alertness], [self.fraction_engage]), axis=0)
        return np.multiply.reduce(_matrix, axis = 0)
    
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
    def formation_vec(self) -> np.array:
        _vector = np.array([u.num_units for u in self.units])
        return _vector
    
    @property
    def offense_matrix(self) -> np.array:
        _matrix = np.vstack([u.offense_vector for u in self.units])
        return _matrix
    
    @property
    def defense_matrix(self) -> np.array:
        _matrix = np.vstack([u.defense_vector for u in self.units])
        _matrix = np.sum(_matrix, axis=0)
        _matrix = np.diag(_matrix)
        return _matrix
    
    def __str__(self) -> str:
        return f"{self.units}"

class Engagement:
    def __init__(self,blue_force, red_force, offensive_side = "blue_force"):
        self.blue_force = blue_force 
        self.red_force = red_force
        self.offensive_side = offensive_side
        
    def decrement_attrition_values(self):
        pass
        
    def salvo(self):
        off = np.matmul(self.blue_force.offense_matrix,\
            self.blue_force.formation_vec)
        defen = np.matmul(self.red_force.defense_matrix,\
             self.red_force.formation_vec )
        return (off - defen)
        
    
    def iter_salvo(self):
        pass
    
if __name__ == "__main__":
    data_a = read_input_file(side=0)
    data_b = read_input_file(side=0)
    a = BattleGroup(data_a, battle_group_name="blue")
    b = BattleGroup(data_b,battle_group_name="red")
    print(vars(Unit))
    
    print("b offense")
    print(b.offense_matrix)
    print("b formation_vec")
    print(b.formation_vec)
    print("b defene matrix")
    print(b.defense_matrix)
    #print(b.units[0].offense_vector)
    e = Engagement(a,b)
    print(e.salvo())
    
    