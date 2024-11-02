import numpy as np
import pandas as pd

def load_data(file_path):
    data = pd.read_csv(file_path, delimiter=',', header=None, index_col=False)
    return data / 4


# Load data
L = load_data('Data/DE_Load.csv')
FL = load_data('Data/DE_F_Load.csv')
FW = load_data('Data/DE_F_Wind.csv')
FS = load_data('Data/DE_F_Solar.csv')
D = load_data('New_data/Dummies_1.csv') * 4

# Data convert to 1 column instead of 24
L_list = []
L_list.extend(L.values.flatten())

L_F_list = []
L_F_list.extend(FL.values.flatten())

W_F_list = []
W_F_list.extend(FW.values.flatten())

S_F_list = []
S_F_list.extend(FS.values.flatten())

# Add dates column
date_range = pd.date_range(start='2015-10-01', periods=35064, freq='H')
data = pd.DataFrame()
data['Dates'] = date_range
data['Dates'] = pd.to_datetime(data['Dates'])

# Add columns of load, wind and solar to dataframe
data['Load'] = L_list
data['Forecast Load'] = L_F_list
data['FW'] = W_F_list
data['FS'] = S_F_list


# Assuming 'Dates' is the column containing datetime information
#data = data[~((data['Dates'].dt.month == 2) & (data['Dates'].dt.day == 29))]

# Data roll
data['X0'] = [1] * 35064 #35040
D_0 = D[0]
D_1 = D[1]
D_2 = D[2]
D_0 = pd.DataFrame(np.repeat(D_0.values, 24, axis=0))
D_1 = pd.DataFrame(np.repeat(D_1.values, 24, axis=0))
D_2 = pd.DataFrame(np.repeat(D_2.values, 24, axis=0))
data['D1'] = D_0
data['D2'] = D_1
data['D3'] = D_2
data['L*'] = [np.nan] * 35064
data['L-1d'] = [np.nan] * 35064
data['FL-1d'] = [np.nan] * 35064
data['L-2d'] = [np.nan] * 35064
data['L-7d'] = [np.nan] * 35064

data['L-1d'] = data['Load'].shift(24)
data['FL-1d'] = data['Forecast Load'].shift(24)
data['L-2d'] = data['Load'].shift(24*2)
data['L-7d'] = data['Load'].shift(24*7)

FL['FL_avg'] = FL.mean(axis=1)
FL_avg = FL['FL_avg']
FL_avg = pd.DataFrame(np.repeat(FL_avg.values, 24, axis=0))
data['FL_avg'] = FL_avg

FL['FL_min'] = FL.min(axis=1)
FL_min = FL['FL_min']
FL_min = pd.DataFrame(np.repeat(FL_min.values, 24, axis=0))
data['FL_min'] = FL_min

FL['FL_max'] = FL.max(axis=1)
FL_max = FL['FL_max']
FL_max = pd.DataFrame(np.repeat(FL_max.values, 24, axis=0))
data['FL_max'] = FL_max


def update_L_star(roL):
    hour_of_day = roL['Dates'].hour

    if hour_of_day <= 10:
        return roL['L-1d']  # Your condition for 'L*' Lhen hour <= 10
    else:
        return roL['FL-1d']  # Your condition for 'L*' Lhen hour > 10


data['L*'] = data.apply(update_L_star, axis=1)
data_final = data[['X0', 'D1', 'D2', 'D3', 'L*', 'L-2d', 'L-7d', 'Forecast Load', 'FW', 'FS', 'FL_avg', 'FL_max', 'FL_min', 'Load']]
data_final.to_csv('New_data/Matrix_load.csv', index=False)
#
