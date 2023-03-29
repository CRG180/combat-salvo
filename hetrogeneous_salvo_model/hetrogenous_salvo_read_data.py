import pandas as pd

def read_input_file(path = "hetrogeneous_salvo_model/hetrogeneous_salvo_data_input_tool.xlsx",
                    side = 0,
                    num_const = 7, 
                    num_array = 15):     
    group = pd.read_excel(path, sheet_name= side, index_col=[0], engine='openpyxl')
    group = [x for _, x in group.groupby('Formations')]
    unit_container = []
    
    for temp in group:
        n = temp.shape[1] # num enemy targets
        unit_dict = {}
        
        for i in range(num_const):
            unit_dict[temp.iloc[i,0]] = temp.iloc[i,1] 
              
        for i in range(num_const, num_array):
            unit_dict[temp.iloc[i,0]] = temp.iloc[i,2:n].to_numpy() 
            
        unit_container.append(unit_dict)
    return unit_container

if __name__ == "__main__":
    data = read_input_file()
    data2 = read_input_file(side = 0)
    print(data)
