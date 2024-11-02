import numpy as np
import pandas as pd

def load_data(file_path):
    data = pd.read_csv(file_path, delimiter=',', header=None, index_col=False)
    return data / 4


# # Load data
L = load_data('Data/DE_Load.csv')
W = load_data('Data/DE_Wind.csv')
S = load_data('Data/DE_Solar.csv')
DA = load_data('Data/BZN_DayAhead.csv') *4

# # Data convert to 1 column instead of 24
L_list = []
L_list.extend(L.values.flatten())

W_list = []
W_list.extend(W.values.flatten())

S_list = []
S_list.extend(S.values.flatten())

DA_list = []
DA_list.extend(DA.values.flatten())

data = pd.DataFrame()

# Add columns of load, wind and solar to dataframe
data['DayAhead'] = DA_list
data['L'] = L_list
data['W'] = W_list
data['S'] = S_list

# Assuming 'Dates' is the column containing datetime information
#data = data[~((data['Dates'].dt.month == 2) & (data['Dates'].dt.day == 29))]

# Data roll
data['X0'] = [1] * 35064 #35040
data['DA-1d'] = [np.nan] * 35064
data['DA-2d'] = [np.nan] * 35064
data['DA-7d'] = [np.nan] * 35064

data['DA-1d'] = data['DayAhead'].shift(24*1)
data['DA-2d'] = data['DayAhead'].shift(24*2)
data['DA-7d'] = data['DayAhead'].shift(24*7)

DA['DA_avg'] = DA.mean(axis=1)
DA_avg = DA['DA_avg']
DA_avg = pd.DataFrame(np.repeat(DA_avg.values, 24, axis=0))
data['DA_avg'] = DA_avg.shift(24)

DA['DA_min'] = DA.min(axis=1)
DA_min = DA['DA_min']
DA_min = pd.DataFrame(np.repeat(DA_min.values, 24, axis=0))
data['DA_min'] = DA_min.shift(24)

DA['DA_max'] = DA.max(axis=1)
DA_max = DA['DA_max']
DA_max = pd.DataFrame(np.repeat(DA_max.values, 24, axis=0))
data['DA_max'] = DA_max.shift(24)

DA['DA_last']= DA.apply(lambda row: row.iloc[-4], axis=1)
DA_last = DA['DA_last']
DA_last = pd.DataFrame(np.repeat(DA_last.values, 24, axis=0))
data['DA_last'] = DA_last.shift(24)

data_final = data[['X0', 'DA-1d', 'DA-2d', 'DA-7d', 'DA_avg', 'DA_min', 'DA_max', 'DA_last', 'L', 'W', 'S', 'DayAhead']]
data_final.to_csv('New_data/Matrix_dayAhead_Real.csv', index=False)

