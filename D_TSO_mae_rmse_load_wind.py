import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error

def load_data(file_path):
    data = pd.read_csv(file_path, delimiter=',', header=None, index_col=False)
    return data /4
def save_data_to_csv(data, file_name):
    data.to_csv(file_name, index=False, header=False)

def add_dates_column(dataframe, start_date='2015-10-01'):
    num_rows = dataframe.shape[0]
    date_range = pd.date_range(start=start_date, periods=num_rows, freq='D')
    dataframe['Dates'] = date_range
    dataframe['Dates'] = pd.to_datetime(dataframe['Dates'])
    return dataframe
def calculate_mae(actual_data, forecast_data, year, name = None):
    year_filter = (actual_data['Dates'] >= f'{year}-10-01') & (actual_data['Dates'] <= f'{year + 1}-09-30')
    actual_year = actual_data.loc[year_filter, range(24)]
    forecast_year = forecast_data.loc[year_filter, range(24)]
    #save_data_to_csv(actual_year, f'TSO_actual_{name}_{year}.csv')
    #save_data_to_csv(forecast_year, f'TSO_forecast_{name}_{year}.csv')
    errors = actual_year.values - forecast_year.values
    mae = np.mean(np.abs(errors))
    return mae
# def calculate_mae(actual_data, forecast_data, year, name = None):
#     year_filter = (actual_data['Dates'] >= f'{year}-10-01') & (actual_data['Dates'] <= f'{year + 1}-09-30')
#     actual_year = actual_data.loc[year_filter, range(24)]
#     # Calculate the average for each row
#     real_average_daily = actual_year.mean(axis=1)
#     # Add a new column 'Average_Daily' to the DataFrame
#     actual_year['Average_Daily'] = real_average_daily
#     forecast_year = forecast_data.loc[year_filter, range(24)]
#     forecast_average_daily = forecast_year.mean(axis=1)
#     forecast_year['Average_Daily'] = forecast_average_daily
#     # Save actual and forecast data to CSV without header
#     save_data_to_csv(actual_year, f'TSO_actual_{name}_{year}.csv')
#     save_data_to_csv(forecast_year, f'TSO_forecast_{name}_{year}.csv')
#     errors = actual_year['Average_Daily'].values - forecast_year['Average_Daily'].values
#     mae = np.mean(np.abs(errors))
#     print(mae)
#     return mae

def calculate_rmse(actual_data, forecast_data, year):
    year_filter = (actual_data['Dates'] >= f'{year}-10-01') & (actual_data['Dates'] <= f'{year + 1}-09-30')
    actual_year = actual_data.loc[year_filter, range(24)]
    forecast_year = forecast_data.loc[year_filter, range(24)]
    rmse = np.sqrt(mean_squared_error(actual_year.values, forecast_year.values))
    return rmse

# Load data
L = load_data('Data/DE_Load.csv')
W = load_data('Data/DE_Wind.csv')

FL = load_data('Data/DE_F_Load.csv')
FW = load_data('Data/DE_F_Wind.csv')

# Add Dates column
dataframes = [L, W, FL, FW]
for df in dataframes:
    df = add_dates_column(df)

# Calculate MAE for Load and Wind
years = [2016, 2017, 2018]
import csv
for year in years:
    mae_load = calculate_mae(L, FL, year, name = 'load')
    mae_wind = calculate_mae(W, FW, year, name = 'wind')

    rmse_load = calculate_rmse(L, FL, year)
    rmse_wind = calculate_rmse(W, FW, year)

    # Display the result for each year
    print(f'MAE for Load ({year}): {mae_load}\n')
    print(f'RMSE for Load ({year}): {rmse_load}\n')
    print(f'MAE for Wind ({year}): {mae_wind}\n')
    print(f'RMSE for Wind ({year}): {rmse_wind}\n')



