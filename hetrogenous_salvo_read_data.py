import pandas as pd

path = "hetrogeneous_salvo_data_input_tool.xlsx"

group = pd.read_excel(path, sheet_name= 0, index_col=[0], engine='openpyxl')
print(group)