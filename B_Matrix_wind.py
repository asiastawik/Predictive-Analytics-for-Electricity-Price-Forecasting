import numpy as np
import pandas as pd

def load_data(file_path):
    data = pd.read_csv(file_path, delimiter=',', header=None, index_col=False)
    return data / 4


# Load data
W = load_data('Data/DE_Wind.csv')
FW = load_data('Data/DE_F_Wind.csv')

# Data convert
W_list = []
W_F_list = []
W_list.extend(W.values.flatten())
W_F_list.extend(FW.values.flatten())
date_range = pd.date_range(start='2015-10-01', periods=35064, freq='H')
data = pd.DataFrame()
data['Dates'] = date_range
data['Dates'] = pd.to_datetime(data['Dates'])
# Assuming 'Dates' is the column containing datetime information
data['Wind'] = W_list
data['Forecast Wind'] = W_F_list
# Assuming 'Dates' is the column containing datetime information
#data = data[~((data['Dates'].dt.month == 2) & (data['Dates'].dt.day == 29))]

# Data roll
data['X0'] = [1] * 35064 #35040
data['W*'] = [np.nan] * 35064
data['W-1d'] = [np.nan] * 35064
data['FW-1d'] = [np.nan] * 35064

data['W-1d'] = data['Wind'].shift(24)
data['FW-1d'] = data['Forecast Wind'].shift(24)

data['FW-1h'] = [np.nan] * 35064
data['FW+1h'] = [np.nan] * 35064

data['FW+1h'] = data['Forecast Wind'].shift(-1)
data['FW-1h'] = data['Forecast Wind'].shift(1)


def update_W_star(row):
    hour_of_day = row['Dates'].hour

    if hour_of_day <= 10:
        return row['W-1d']  # Your condition for 'W*' when hour <= 10
    else:
        return row['FW-1d']  # Your condition for 'W*' when hour > 10


data['W*'] = data.apply(update_W_star, axis=1)
data_final = data[['X0', 'W*', 'Forecast Wind', 'FW-1h', 'FW+1h', 'Wind']]
data_final.to_csv('New_data/Matrix_wind.csv', index=False)

