import numpy as np
import pandas as pd

def load_data(file_path):
    data = pd.read_csv(file_path, delimiter=',', header=0, index_col=False)
    return data

start_day = 366+365
end_day = 731+365
data = load_data('New_data/Matrix_Intraday2_Enhanced.csv')
X_full = data.iloc[start_day*24:end_day*24,-1]
windows = [365]
forecasts_window_lists=[]

for window in windows:
    forecast_list=[]
    for h in range(24):
        data_day = data[h::24]
        X0 = data_day['X0'].values.tolist()
        X1 = data_day['DA_Forecast'].values.tolist()
        X2 = data_day['ID*'].values.tolist()
        X3 = data_day['L'].values.tolist()
        X4 = data_day['W'].values.tolist()
        X5 = data_day['S'].values.tolist()
        X6 = data_day['L-FL'].values.tolist()
        X7 = data_day['W-FW'].values.tolist()
        X8 = data_day['S-FS'].values.tolist()
        X9 = data_day['L-FL_1d'].values.tolist()
        X10 = data_day['W-FW_1d'].values.tolist()
        X11 = data_day['S-FS_1d'].values.tolist()
        Y = data_day[['Intraday']].values.tolist()
        for d in range(start_day,end_day):  # Adjust the range as needed 731
            Y_subset = Y[d - window:d]
            X0_subset = X0[d - window:d]
            X1_subset = X1[d - window:d]
            X2_subset = X2[d - window:d]
            X3_subset = X3[d - window:d]
            X4_subset = X4[d - window:d]
            X5_subset = X5[d - window:d]
            X6_subset = X6[d - window:d]
            X7_subset = X7[d - window:d]
            X8_subset = X8[d - window:d]
            X9_subset = X9[d - window:d]
            X10_subset = X10[d - window:d]
            X11_subset = X11[d - window:d]
            X = np.column_stack([X0_subset, X1_subset, X2_subset, X3_subset, X4_subset, X5_subset, X6_subset, X7_subset, X8_subset, X9_subset, X10_subset, X11_subset])
            betas, _, _, _ = np.linalg.lstsq(X, Y_subset, rcond=None)
            X_fut = np.array([1, X1[d], X2[d], X3[d], X4[d], X5[d], X6[d], X7[d], X8[d], X9[d], X10[d], X11[d]])
            forecast = np.dot(X_fut, betas)
            forecast_list.append(forecast)
    flattened_forecast_list = [item for sublist in forecast_list for item in sublist]
    forecasts_window_lists.append(flattened_forecast_list)

# Create a DataFrame
df = pd.DataFrame({
    '365': forecasts_window_lists[0],
})
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
# Combine all rows into a single list
combined_list = new_df.values.flatten().tolist()


# Create a DataFrame
returning = pd.DataFrame({'Final': combined_list})
print(returning)
returning.to_csv('New_data/Forecast_Intraday2_Enhanced.csv', index=False, header = None)

#print(combined_list[:-1])
X_full = X_full.values.flatten().tolist()
errors = [a - b for a, b in zip(X_full[:-1], combined_list[:-1])]
mae = np.mean(np.abs(errors))
print(round(mae,3))
rmse = np.sqrt(np.mean(np.square(errors)))
print(round(rmse,3))