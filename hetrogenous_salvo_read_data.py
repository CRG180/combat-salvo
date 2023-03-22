import pandas as pd

path = "hetrogeneous_salvo_data_input_tool.xlsx"

group = pd.read_excel(path, sheet_name= 0, index_col=[0], engine='openpyxl')
group = [x for _, x in group.groupby('Formations')]

for x in range(len(group)):
    temp = group[x]
    n = group[x].shape[1] # num enemy targets
    unit_dict = {}
    num_const = 4
    num_array = 12
    for i in range(num_const):
        unit_dict[temp.iloc[i,0]] = temp.iloc[i,1]
        
    for i in range(num_const, num_array):
        unit_dict[temp.iloc[i,0]] = temp.iloc[i,2:n].to_numpy() # not complete this is wrong

    print(unit_dict)