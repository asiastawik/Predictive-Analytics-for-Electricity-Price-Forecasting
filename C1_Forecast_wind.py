import numpy as np
import pandas as pd

def load_data(file_path):
    data = pd.read_csv(file_path, delimiter=',', header=0, index_col=False)
    return data

start_day = 366# + 365 +365
end_day = 731 #+365 +365
data = load_data('New_data/Matrix_wind.csv')
X_full = data.iloc[start_day*24:end_day*24,-1]
windows = [56, 84, 112, 351, 358, 365]
forecasts_window_lists=[]
for window in windows:
    forecast_list = []
    for h in range(24):
        data_day = data[h::24]
        X0 = data_day[['X0']].values.tolist()
        X1 = data_day['W*'].values.tolist()
        X2 = data_day[['Forecast Wind']].values.tolist()
        X3 = data_day[['FW-1h']].values.tolist()
        X4 = data_day[['FW+1h']].values.tolist()
        Y = data_day[['Wind']].values.tolist()
        for d in range(start_day, end_day):  # Adjust the range as needed
            Y_subset = Y[d - window:d]
            X0_subset = X0[d - window:d]
            X1_subset = X1[d - window:d]
            X2_subset = X2[d - window:d]
            X3_subset = X3[d - window:d]
            X4_subset = X4[d - window:d]
            X = np.column_stack([X0_subset, X1_subset, X2_subset, X3_subset, X4_subset])
            #arr1 = np.linalg.inv(np.dot(X.T, X))
            betas, _, _, _ = np.linalg.lstsq(X, Y_subset, rcond=None)
            X_fut = np.array([1, X1[d], X2[d][0], X3[d][0], X4[d][0]])
            forecast = np.dot(X_fut, betas)
            forecast_list.append(forecast)
    flattened_forecast_list = [item for sublist in forecast_list for item in sublist]
    forecasts_window_lists.append(flattened_forecast_list)

# Create a DataFrame
df = pd.DataFrame({
    '56': forecasts_window_lists[0],
    '84': forecasts_window_lists[1],
    '112': forecasts_window_lists[2],
    '351': forecasts_window_lists[3],
    '358': forecasts_window_lists[4],
    '365': forecasts_window_lists[5],
})
df.index = range(start_day*24, (end_day)*24)
df['Avg'] = df.mean(axis=1) #1godzina 1, 2, .., 365 dni, 2godizna:...
avg = df['Avg'].reset_index()
avg = avg['Avg']

# Zmiana Forecastu na dataframe
num_columns = 24
num_values_per_column = len(avg) // num_columns
new_columns = {}
for i in range(num_columns):
    start_index = i * num_values_per_column
    end_index = (i + 1) * num_values_per_column
    new_columns[f'Column_{i+1}'] = avg.iloc[start_index:end_index].values
new_df = pd.DataFrame(new_columns)
#new_df.to_csv('New_data/Forecast_wind_enhanced_2016.csv', index=False,  header=False)
# Combine all rows into a single list
combined_list = new_df.values.flatten().tolist()
X_full = X_full.values.flatten().tolist()
# przy robieniu forecast dla 2018 nalezy dodac '[:-1]' do obu list w zipie
# poniewaz forecast jest z elementem predykcji na godzine do przodu a tej danej nie mamy
errors = [a - b for a, b in zip(X_full[:-1], combined_list[:-1])]
mae = np.mean(np.abs(errors))
print(mae)
rmse = np.sqrt(np.mean(np.square(errors)))
print(rmse)


