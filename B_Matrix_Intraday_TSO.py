import numpy as np
import pandas as pd

def load_data(file_path):
    data = pd.read_csv(file_path, delimiter=',', header=None, index_col=False)
    return data / 4


# # Load data
FL = load_data('Data/DE_F_Load.csv')
FW = load_data('Data/DE_F_Wind.csv')
FS = load_data('Data/DE_F_Solar.csv')
DA = load_data('Data/BZN_DayAhead.csv') *4
ID = load_data('Data/Intraday.csv') *4

# # Data convert to 1 column instead of 24
L_F_list = []
L_F_list.extend(FL.values.flatten())

W_F_list = []
W_F_list.extend(FW.values.flatten())

S_F_list = []
S_F_list.extend(FS.values.flatten())

DA_list = []
DA_list.extend(DA.values.flatten())

ID_list = []
ID_list.extend(ID.values.flatten())

data = pd.DataFrame()

# Add columns of load, wind and solar to dataframe
data['DayAhead'] = DA_list
data['Intraday'] = ID_list
data['FL'] = L_F_list
data['FW'] = W_F_list
data['FS'] = S_F_list

# Assuming 'Dates' is the column containing datetime information
#data = data[~((data['Dates'].dt.month == 2) & (data['Dates'].dt.day == 29))]

# Data roll
data['X0'] = [1] * 35064 #35040
data['ID*'] = [np.nan] * 35064
data['ID-1d'] = [np.nan] * 35064
data['DA-1d'] = [np.nan] * 35064
data['ID-2d'] = [np.nan] * 35064
data['ID-7d'] = [np.nan] * 35064

data['ID-1d'] = data['Intraday'].shift(24*1)
data['DA-1d'] = data['DayAhead'].shift(24*1)
data['ID-2d'] = data['Intraday'].shift(24*2)
data['ID-7d'] = data['Intraday'].shift(24*7)

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

# Add dates column
date_range = pd.date_range(start='2015-10-01', periods=35064, freq='H')
data['Dates'] = date_range
data['Dates'] = pd.to_datetime(data['Dates'])

def update_L_star(roL):
    hour_of_day = roL['Dates'].hour

    if hour_of_day <= 10:
        return roL['ID-1d']  # Your condition for 'L*' Lhen hour <= 10
    else:
        return roL['DA-1d']  # Your condition for 'L*' Lhen hour > 10

data['ID*'] = data.apply(update_L_star, axis=1)

data_final = data[['X0', 'ID*', 'ID-2d', 'ID-7d', 'DA_avg', 'DA_min', 'DA_max', 'DA_last', 'FL', 'FW', 'FS', 'Intraday']]
data_final.to_csv('New_data/Matrix_Intraday_TSO.csv', index=False)

