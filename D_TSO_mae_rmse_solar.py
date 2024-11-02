import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error

def load_data(file_path):
    data = pd.read_csv(file_path, delimiter=',', header=None, index_col=False)
    return data /4

def add_dates_column(dataframe, start_date='2015-10-01'):
    num_rows = dataframe.shape[0]
    date_range = pd.date_range(start=start_date, periods=num_rows, freq='D')
    dataframe['Dates'] = date_range
    dataframe['Dates'] = pd.to_datetime(dataframe['Dates'])
    return dataframe

def filter_years(actual_data, forecast_data, years):
    filtered_data = []
    for year in years:
        year_filter = (actual_data['Dates'] >= f'{year}-10-01') & (actual_data['Dates'] <= f'{year + 1}-09-30')
        filtered_actual = actual_data[year_filter].reset_index(drop=True)
        filtered_forecast = forecast_data[year_filter].reset_index(drop=True)
        filtered_data.append(filtered_actual)
        filtered_data.append(filtered_forecast)
    return filtered_data

S = load_data('Data/DE_Solar.csv')
FS = load_data('Data/DE_F_Solar.csv')

dataframes = [S, FS]
for df in dataframes:
    df = add_dates_column(df)

s_fs = filter_years(S, FS, [2016,2017,2018])
S_2016 = s_fs[0]
FS_2016 = s_fs[1]
S_2017 = s_fs[2]
FS_2017 = s_fs[3]
S_2018 = s_fs[4]
FS_2018 = s_fs[5]

FS_new_2016 = FS_2016.iloc[:, list(range(7,17))]

FS_new_2017 = FS_2017.iloc[:, list(range(7,17))]

FS_new_2018 = FS_2018.iloc[:, list(range(7,17))]

S_new_2016 = S_2016.iloc[:, list(range(7,17))]

S_new_2017 = S_2017.iloc[:, list(range(7,17))]

S_new_2018 = S_2018.iloc[:, list(range(7,17))]

# #erase timestamps
# S_2016 = [item for item in S_2016 if not isinstance(item, pd.Timestamp)]
# FS_2016 = [item for item in FS_2016 if not isinstance(item, pd.Timestamp)]
# S_2017 = [item for item in S_2017 if not isinstance(item, pd.Timestamp)]
# FS_2017 = [item for item in FS_2017 if not isinstance(item, pd.Timestamp)]
# S_2018 = [item for item in S_2018 if not isinstance(item, pd.Timestamp)]
# FS_2018 = [item for item in FS_2018 if not isinstance(item, pd.Timestamp)]

S_2016 = S_new_2016.values.flatten() # change S to a list
FS_2016 = FS_new_2016.values.flatten() # change FS to a list
S_2017 = S_new_2017.values.flatten()# change S to a list
FS_2017 = FS_new_2017.values.flatten() # change FS to a list
S_2018 = S_new_2018.values.flatten()# change S to a list
FS_2018 = FS_new_2018.values.flatten()# change FS to a list

# Assuming S_2016 and FS_2016 are lists
S_2016 = np.array(S_2016)
FS_2016 = np.array(FS_2016)

S_2017 = np.array(S_2017)
FS_2017 = np.array(FS_2017)

S_2018 = np.array(S_2018)
FS_2018 = np.array(FS_2018)

mae_2016 = np.mean(np.abs(S_2016 - FS_2016))
rmse_2016 = np.sqrt(mean_squared_error(S_2016, FS_2016))

mae_2017 = np.mean(np.abs(S_2017 - FS_2017))
mae_2018 = np.mean(np.abs(S_2018 - FS_2018))

rmse_2016 = np.sqrt(mean_squared_error(S_2016, FS_2016))
rmse_2017 = np.sqrt(mean_squared_error(S_2017, FS_2017))
rmse_2018 = np.sqrt(mean_squared_error(S_2018, FS_2018))



print(round(mae_2016,3))
print(round(mae_2017,3))
print(round(mae_2018,3))

print(round(rmse_2016,3))
print(round(rmse_2017,3))
print(round(rmse_2018,3))
