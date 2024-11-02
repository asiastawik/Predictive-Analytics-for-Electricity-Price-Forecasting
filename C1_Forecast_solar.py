import numpy as np
import pandas as pd
from scipy import stats


def load_data(file_path):
    data = pd.read_csv(file_path, delimiter=',', header=0, index_col=False)
    return data

start_day = 366 + 365 +365
end_day = 731 +365 +365
data = load_data('New_data/Matrix_solar.csv')
X_full = data.iloc[start_day*24:end_day*24,-1]
windows = [56, 84, 112, 351, 358, 365]
forecasts_window_lists=[]
for window in windows:
    forecast_list=[]
    for h in range(24):
        data_day = data[h::24]
        X0 = data_day[['X0']].values.tolist()
        X1 = data_day[['XS']].values.tolist()
        X2 = data_day['S*'].values.tolist()
        X3 = data_day[['Forecast Solar']].values.tolist()
        X4 = data_day[['FS-1h']].values.tolist()
        X5 = data_day[['FS+1h']].values.tolist()
        Y = data_day[['Solar']].values.tolist()
        for d in range(start_day, end_day):
            Y_subset = Y[d - window:d]
            X0_subset = X0[d - window:d]
            X1_subset = X1[d - window:d]
            X2_subset = X2[d - window:d]
            X3_subset = X3[d - window:d]
            X4_subset = X4[d - window:d]
            X5_subset = X5[d - window:d]
            X = np.column_stack([X0_subset, X1_subset, X2_subset, X3_subset, X4_subset, X5_subset])
            betas , _, _, _ = np.linalg.lstsq(X, Y_subset, rcond=None)
            X_fut = np.array([1, X1[d][0], X2[d], X3[d][0], X4[d][0], X5[d][0]])
            forecast = np.dot(X_fut, betas)
            if forecast >0:
                forecast_list.append(forecast)
            else:
                forecast_list.append([0])
    flattened_forecast_list = [item for sublist in forecast_list for item in sublist]
    forecasts_window_lists.append(flattened_forecast_list)

df = pd.DataFrame({
    '56': forecasts_window_lists[0],
    '84': forecasts_window_lists[1],
    '112': forecasts_window_lists[2],
    '351': forecasts_window_lists[3],
    '358': forecasts_window_lists[4],
    '365': forecasts_window_lists[5],
})
print(df)
df.index = range(start_day*24, end_day*24)
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
#new_df.to_csv('New_data/Forecast_solar_enhanced_2018.csv', index=False,  header=False)
# Combine all rows into a single list
combined_list = new_df.values.flatten().tolist()
X_full = X_full.values.flatten().tolist()
errors = [a - b for a, b in zip(X_full, combined_list)]
# Bierzemy tylko errory dla godzin 7-16 wlacznie
elements_to_take = [7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
# Create sublists with 24 elements each
sublists = [errors[i:i+24] for i in range(0, len(errors), 24)]
# Extract the desired elements from each sublist and append to a final list
final_list = [sublist[index] for sublist in sublists for index in elements_to_take]

mae = np.mean(np.abs(final_list))
print(mae)
rmse = np.sqrt(np.mean(np.square(final_list)))
print(rmse)


