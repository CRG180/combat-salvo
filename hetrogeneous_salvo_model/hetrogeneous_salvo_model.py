from hetrogenous_salvo_read_data import read_input_file
import numpy as np
import warnings

def check_0_1(input, formation):
    for i in input:
        if i < 0 or i > 1:
            raise Exception(f"{formation}: Value is less than O or greater than 1 --- {input}")
        else:
            continue
        
def sum_1(input, formation):
    if sum(input) > 1:
        raise Exception(f"{formation}: Vector sum is greater than 1 --- {input}")
    if sum(input) < 0:
        Exception(f"{formation}: Vector sum is less than 0 --- {input}")
    if sum(input) != 1:
        warnings.warn(f"{formation}: Vector does not sum to 1 --- {input}")              


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
        
        for i in [self.fraction_engage]:
            sum_1(i, self.formation)
        
        for i in [self.scouting, self.alertness, self.training, self.distraction]:
            check_0_1(i, self.formation)
    
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
        
    def salvo(self):
        off = np.matmul(self.blue_force.offense_matrix,\
            self.blue_force.formation_vec)
        defen = np.matmul(self.red_force.defense_matrix,\
             self.red_force.formation_vec )
        return (off - defen)
        
    def decrement_attrition_values(self):
        pass
    
    def iter_salvo(self):
        pass
    
if __name__ == "__main__":
    data_a = read_input_file(side=0)
    data_b = read_input_file(side=0)
    a = BattleGroup(data_a, battle_group_name="blue")
    b = BattleGroup(data_b,battle_group_name="red")
    print("b offense")
    print(b.offense_matrix)
    print("b formation_vec")
    print(b.formation_vec)
    print("b defene matrix")
    print(b.defense_matrix)
    #print(b.units[0].offense_vector)
    e = Engagement(a,b)
    print(e.salvo())
    