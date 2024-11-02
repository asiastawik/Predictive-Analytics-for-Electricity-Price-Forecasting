import numpy as np
import pandas as pd

def load_data(file_path):
    data = pd.read_csv(file_path, delimiter=',', header=None, index_col=False)
    return data / 4


# # Load data
L0 = load_data('Data/DE_Load.csv') #2015
L1 = load_data('New_data/Forecast_load_enhanced_2016.csv') *4 # 2016
L2 = load_data('New_data/Forecast_load_enhanced_2017.csv') *4 # 2017
L3 = load_data('New_data/Forecast_load_enhanced_2018.csv') *4 # 2018
L = pd.concat([L0[:366], L1, L2, L3], ignore_index=True)
W0 = load_data('Data/DE_Wind.csv') # te zmienic na enhanced
W1 = load_data('New_data/Forecast_wind_enhanced_2016.csv') *4 # 2016
W2 = load_data('New_data/Forecast_wind_enhanced_2017.csv') *4 # 2017
W3 = load_data('New_data/Forecast_wind_enhanced_2018.csv') *4 # 2018
W = pd.concat([W0[:366], W1, W2, W3], ignore_index=True)
S0 = load_data('Data/DE_Solar.csv')  # te zmienic na enhanced
S1 = load_data('New_data/Forecast_solar_enhanced_2016.csv') *4 # 2016
S2 = load_data('New_data/Forecast_solar_enhanced_2017.csv') *4 # 2017
S3 = load_data('New_data/Forecast_solar_enhanced_2018.csv') *4 # 2018
S = pd.concat([S0[:366], S1, S2, S3], ignore_index=True)
FL = load_data('Data/DE_F_Load.csv')
FW = load_data('Data/DE_F_Wind.csv')
FS = load_data('Data/DE_F_Solar.csv')
DA = load_data('Data/BZN_DayAhead.csv') *4
DA_Forecast = load_data('New_data/Forecast_dayAhead_enhanced_2017_2018.csv') * 4
DA_Forecast = pd.concat([DA[:731], DA_Forecast], ignore_index=True)
print(DA_Forecast)
ID = load_data('Data/Intraday.csv') *4

# # Data convert to 1 column instead of 24
L_list = []
L_list.extend(L.values.flatten())

W_list = []
W_list.extend(W.values.flatten())

S_list = []
S_list.extend(S.values.flatten())

FL_list = []
FL_list.extend(FL.values.flatten())

FW_list = []
FW_list.extend(FW.values.flatten())

FS_list = []
FS_list.extend(FS.values.flatten())

DA_list = []
DA_list.extend(DA.values.flatten())

ID_list = []
ID_list.extend(ID.values.flatten())

DA_Forecast_list = []
DA_Forecast_list.extend(DA_Forecast.values.flatten())


# Add dates column
date_range = pd.date_range(start='2015-10-01', periods=35064, freq='H')
data = pd.DataFrame()
data['Dates'] = date_range
data['Dates'] = pd.to_datetime(data['Dates'])


# Add columns of load, wind and solar to dataframe
data['DayAhead'] = DA_list
data['Intraday'] = ID_list
data['L'] = L_list
data['W'] = W_list
data['S'] = S_list
data['FL'] = FL_list
data['FW'] = FW_list
data['FS'] = FS_list
data['DA_Forecast'] = DA_Forecast_list

# Assuming 'Dates' is the column containing datetime information
#data = data[~((data['Dates'].dt.month == 2) & (data['Dates'].dt.day == 29))]

# Data roll
data['X0'] = [1] * 35064 #35040
data['ID*'] = [np.nan] * 35064
data['ID-1d'] = [np.nan] * 35064
data['DA-1d'] = [np.nan] * 35064

data['ID-1d'] = data['Intraday'].shift(24*1)
data['DA-1d'] = data['DayAhead'].shift(24*1)
data['L-1d'] = data['L'].shift(24*1)
data['FL-1d'] = data['FL'].shift(24*1)
data['W-1d'] = data['W'].shift(24*1)
data['FW-1d'] = data['FW'].shift(24*1)
data['S-1d'] = data['S'].shift(24*1)
data['FS-1d'] = data['FS'].shift(24*1)

def update_L_star(roL):
    hour_of_day = roL['Dates'].hour

    if hour_of_day <= 10:
        return roL['ID-1d']  # Your condition for 'L*' Lhen hour <= 10
    else:
        return roL['DA-1d']  # Your condition for 'L*' Lhen hour > 10

data['ID*'] = data.apply(update_L_star, axis=1)

data['L-FL'] = data['L']-data['FL']
data['W-FW'] = data['W']-data['FW']
data['S-FS'] = data['S']-data['FS']
data['L-FL_1d'] = data['L-1d']-data['FL-1d']
data['W-FW_1d'] = data['W-1d']-data['FW-1d']
data['S-FS_1d'] = data['S-1d']-data['FS-1d']


data_final = data[['X0', 'DA_Forecast', 'ID*', 'L', 'W', 'S', 'L-FL', 'W-FW', 'S-FS', 'L-FL_1d','W-FW_1d','S-FS_1d', 'Intraday']]
data_final.to_csv('New_data/Matrix_Intraday2_Enhanced.csv', index=False)

