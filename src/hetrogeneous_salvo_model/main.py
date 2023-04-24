
from utils import read_input_file
from battleGroup import BattleGroup
from engagement import SimultaneousSalvo


if __name__ == "__main__":
    file_path = "src/hetrogeneous_salvo_model/data/hetrogeneous_salvo_data_input_tool_v3.xlsx"
    data_a = read_input_file( path = file_path,side=0)
    data_b = read_input_file(path = file_path,side=1)
    a = BattleGroup(data_a, battle_group_name="B Force")
    b = BattleGroup(data_b,battle_group_name="A Force")
    print("A offense")
    print(b.offense_matrix)
    print("B offense")
    print(a.offense_matrix)
    print("A formation_vec")
    print(b.formation_vec)
    print("B formation_vec")
    print(a.formation_vec)
    print("B Def Mat")
    print(a.defense_matrix)
    print("A def matrix")
    print(b.defense_matrix)

    e = SimultaneousSalvo(a,b)
    e.iter_salvo()