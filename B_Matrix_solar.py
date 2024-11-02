import numpy as np
import pandas as pd

def load_data(file_path):
    data = pd.read_csv(file_path, delimiter=',', header=None, index_col=False)
    return data / 4

# Load data
S = load_data('Data/DE_Solar.csv')
FS = load_data('Data/DE_F_Solar.csv')
SH = pd.read_csv('Data/Sun_hours.csv', header=None, index_col=False)
SH = pd.DataFrame(np.repeat(SH.values, 24, axis=0), columns=SH.columns) /24

# Data convert
S_list = []
S_F_list = []
S_list.extend(S.values.flatten())
S_F_list.extend(FS.values.flatten())
date_range = pd.date_range(start='2015-10-01', periods=35064, freq='H')
data = pd.DataFrame()
data['Dates'] = date_range
data['Dates'] = pd.to_datetime(data['Dates'])
# Assuming 'Dates' is the column containing datetime information
data['Solar'] = S_list
data['Forecast Solar'] = S_F_list
# Assuming 'Dates' is the column containing datetime information
#data = data[~((data['Dates'].dt.month == 2) & (data['Dates'].dt.day == 29))]

# Data roll
data['X0'] = [1] * 35064 #35040
data['XS'] = SH
data['S*'] = [np.nan] * 35064
data['S-1d'] = [np.nan] * 35064
data['FS-1d'] = [np.nan] * 35064

data['S-1d'] = data['Solar'].shift(24)
data['FS-1d'] = data['Forecast Solar'].shift(24)

data['FS-1h'] = [np.nan] * 35064
data['FS+1h'] = [np.nan] * 35064

data['FS+1h'] = data['Forecast Solar'].shift(-1)
data['FS-1h'] = data['Forecast Solar'].shift(1)


def update_S_star(roS):
    hour_of_day = roS['Dates'].hour

    if hour_of_day <= 10:
        return roS['S-1d']  # Your condition for 'S*' Shen hour <= 10
    else:
        return roS['FS-1d']  # Your condition for 'S*' Shen hour > 10


data['S*'] = data.apply(update_S_star, axis=1)
data_final = data[['X0', 'XS', 'S*', 'Forecast Solar', 'FS-1h', 'FS+1h', 'Solar']]
data_final.to_csv('New_data/Matrix_solar.csv', index=False)

