import numpy as np
import pandas as pd

# Laczenie forecast load 2017 i 2018
lr15 = pd.read_csv('Data\DE_Load.csv',header=None)
csv1a = pd.read_csv('New_data\Forecast_load_enhanced_2016.csv',header=None)
csv1 = pd.read_csv('New_data\Forecast_load_enhanced_2017.csv',header=None)
csv2 = pd.read_csv('New_data\Forecast_load_enhanced_2018.csv',header=None)
FL = pd.concat([lr15[:366],csv1a,csv1, csv2], ignore_index=True)

# Laczenie forecast wind 2017 i 2018
wr15 = pd.read_csv('Data\DE_Wind.csv',header=None)
csv3a = pd.read_csv('New_data\Forecast_wind_enhanced_2016.csv',header=None)
csv3 = pd.read_csv('New_data\Forecast_wind_enhanced_2017.csv',header=None)
csv4 = pd.read_csv('New_data\Forecast_wind_enhanced_2018.csv',header=None)
FW = pd.concat([wr15[:366],csv3a,csv3, csv4], ignore_index=True)

# Laczenie forecast solar 2017 i 2018
sr15 = pd.read_csv('Data\DE_Solar.csv',header=None)
csv5a = pd.read_csv('New_data\Forecast_solar_enhanced_2016.csv',header=None)
csv5 = pd.read_csv('New_data\Forecast_solar_enhanced_2017.csv',header=None)
csv6 = pd.read_csv('New_data\Forecast_solar_enhanced_2018.csv',header=None)
FS = pd.concat([sr15[:366],csv5a,csv5, csv6], ignore_index=True)

DA = pd.read_csv('Data/BZN_DayAhead.csv', delimiter=',', header=None, index_col=False) #2015-2019
DA['Avg'] = DA.mean(axis=1)
DA['Min'] = DA.min(axis=1)
DA['Max'] = DA.max(axis=1)
DA['Last'] = DA[23]

L_F_list = []
L_F_list.extend(FL.values.flatten())

W_F_list = []
W_F_list.extend(FW.values.flatten())

S_F_list = []
S_F_list.extend(FS.values.flatten())

DA_list = []
DA_list.extend(DA.iloc[:,0:24].values.flatten())  # lista DA 2015- 2019
data = pd.DataFrame()

# Add columns of load, wind and solar to dataframe
data['DayAhead'] = DA_list[:] # od 2016 DA
data['FL'] = L_F_list
data['FW'] = W_F_list
data['FS'] = S_F_list

# Data roll
data['X0'] = [1] * 35064
data['DA-1d'] = [np.nan] * 35064
data['DA-2d'] = [np.nan] * 35064 #26280
data['DA-7d'] = [np.nan] * 35064

data['DA-1d'] = data['DayAhead'].shift(24*1)
data['DA-2d'] = data['DayAhead'].shift(24*2)
data['DA-7d'] = data['DayAhead'].shift(24*7)

DA_avg = pd.DataFrame(np.repeat(DA['Avg'].values, 24, axis=0))
data['DA_avg'] = DA_avg.shift(24)

DA_min = pd.DataFrame(np.repeat(DA['Min'].values, 24, axis=0))
data['DA_min'] = DA_min.shift(24)

DA_max = pd.DataFrame(np.repeat(DA['Max'].values, 24, axis=0))
data['DA_max'] = DA_max.shift(24)

DA_last = pd.DataFrame(np.repeat(DA['Last'].values, 24, axis=0))
data['DA_last'] = DA_last.shift(24)

data_final = data[['X0', 'DA-1d', 'DA-2d', 'DA-7d', 'DA_avg', 'DA_min', 'DA_max', 'DA_last', 'FL', 'FW', 'FS', 'DayAhead']]
data_final.to_csv('New_data/Matrix_dayAhead_Enhanced.csv', index=False)
