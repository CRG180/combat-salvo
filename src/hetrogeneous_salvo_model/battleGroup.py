#!/usr/bin/env python3

import numpy as np
from unit import Unit


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
    def staying_power_vec(self) -> np.array:
        _vector = np.array([u.staying_power for u in self.units])
        return _vector
    
    @property
    def offense_matrix(self) -> np.array:
        _matrix = np.vstack([u.offense_vector for u in self.units])
        return np.transpose(_matrix)
    
    @property
    def defense_matrix(self) -> np.array:
        _matrix = np.vstack([u.defense_vector for u in self.units])
        _matrix = np.sum(_matrix, axis=1)
        _matrix = np.diag(_matrix)
        return _matrix
    
    def __str__(self) -> str:
        return "\n".join(f"{unit.formation} -- {unit.num_units}" for unit in self.units)

if __name__ == "__main__":
    pass