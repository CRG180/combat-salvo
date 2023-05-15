#!/usr/bin/env python3

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
    """A class to provide data for a single unit for a heterogeous model.  
    
	...
 
	Attributes
    ----------
    
    formation: str
		unit formation's name
    type: str
        type class e.g. rocket company
    mgrs: str
        position in MRGS cordinates
    range: int
        max offensive weapon range
	num_units: int
		number of units in the formation
    num_missiles_off int
        number of offensive missiles available
    num_missiles_def int
        number of defensive missiles available
	aimed_offense: int
		the number of well-aimed missiles fired by each unit per enemey target per salvo.
    fraction_engage: num
        fraction the units that engage each enemy target {[0,1]}
	defense_capability: int
		 number of well-aimed attacking missiles eliminated by each unit per salvo.
	staying: int
		 number of missiles required to place an unit out of action.
	scouting: num
		 scouting effectiveness against each enemy unit {[0,1]}.
	alertness: num
		 defender alertness against each enemy unit [0,1].
	training: num
		training effectiveness against each enemy unit [0,1].
	distraction: num
		distraction factor against each enemy unit [0,1].
	
	Methods
    -------
	__sub__(self, other):
		'Method overload for to decrment the number of units during 
        engagment

	"""
 
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
    def unit_dead(self) -> bool:
        if self.num_units > 0:
            return False
        else:
            return True 
    
    @property
    def offense_shots_available(self) -> float:
        return self.num_units * self.num_missiles_off
        
    @property
    def defense_shots_available(self) -> float:
        return self.num_units * self.num_missiles_def
      
    @property
    def offense_vector(self) -> np.array: # check this 
        _matrix = np.concatenate(([self.aimed_offense , self.scouting], \
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

if __name__ == "__main__":
    pass