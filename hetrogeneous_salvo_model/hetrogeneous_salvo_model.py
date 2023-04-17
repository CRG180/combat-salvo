from hetrogenous_salvo_read_data import read_input_file
import numpy as np
import warnings

def check_0_1(input, formation):
    '''Checks Unit class input vectors to ensure each value
    is between O and 1'''
    for i in input:
        if i < 0 or i > 1:
            raise Exception(f"{formation}: Value is less than O or greater than 1 --- {input}")
        else:
            continue
        
def sum_1(input, formation):
    '''Check Unit class input vectors to ensure it sums to or less than the value of 1.
    Vector sums cannot be negative. A warning is given when values does not sum to 1'''
    if sum(input) > 1:
        raise Exception(f"{formation}: Vector sum is greater than 1 --- {input}")
    if sum(input) < 0:
        raise Exception(f"{formation}: Vector sum is less than 0 --- {input}")
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
        self.defense_capability = unit_dict["defense_capability"]
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
    def offense_shots_available(self) -> float:
        return self.num_units * self.num_missiles_off
        
    @property
    def defense_shots_available(self) -> float:
        return self.num_units * self.num_missiles_def
      
    @property
    def offense_vector(self) -> np.array: # check this 
        _matrix = np.concatenate(([self.scouting], \
		[self.training],[self.distraction],[self.fraction_engage]),\
		axis = 0)	
        return np.multiply.reduce(_matrix, axis=0)
    
    @property
    def defense_vector(self)-> np.array: # parameters need to be rechecked
        _matrix = np.concatenate(([self.defense_capability], \
            [self.alertness]), axis=0)
        return np.multiply.reduce(_matrix, axis = 0)

    def __sub__(self, other) -> None:
        '''Method overload for to decrment the number of units during 
        engagment. The conditional prevents the number of units being negative'''
        _last_value = self.num_units
        self.num_units -= other
        if self.num_units > _last_value:
            warnings.warn(f"{self.formation}: __Sub__ resulted in greater number than last iter")
        if self.num_units < 0:
            self.num_units = 0 
        return None
    
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
        return "\n".join(f"{unit.formation} -- {unit.num_units}" for unit in self.units)


class Engagement:
    
    def __init__(self,blue_force, red_force, offensive_side = "blue_force"):
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
            
            _red_attrit_vec = off-defen
            print(f"{self.iter_num} -- _red_attrit_vec {_red_attrit_vec }" )

            return _red_attrit_vec

        if self._offensive_side == "red_force":
            
            off = np.matmul(self.red_force.offense_matrix,\
                self.red_force.formation_vec)
            
            defen = np.matmul(self.blue_force.defense_matrix,\
                self.blue_force.formation_vec )
            
            _blue_attrit_vec = off-defen
            print(f"{self.iter_num} -- _blue_attrit_vec {_blue_attrit_vec }" )
            
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
            
            print(f"------ Salvo Iteration {self.iter_num} Battle compelte {self.battle_complete} --------")
            
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
    data_a = read_input_file(side=0)
    data_b = read_input_file(side=1)
    a = BattleGroup(data_a, battle_group_name="blue")
    b = BattleGroup(data_b,battle_group_name="red")
    print("Red offense")
    print(b.offense_matrix)
    print("Blue offense")
    print(a.offense_matrix)
    print("Red formation_vec")
    print(b.formation_vec)
    print("Blue formation_vec")
    print(a.formation_vec)
    print("Blue Def Mat")
    print(a.defense_matrix)
    print("red def matrix")
    print(b.defense_matrix)

    e = SimultaneousSalvo(a,b)
    e.iter_salvo()
    
    
