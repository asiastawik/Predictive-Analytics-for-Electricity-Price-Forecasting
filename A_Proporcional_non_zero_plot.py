import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams
import numpy as np
# initial parameters of plots
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Times New Roman']
rcParams['font.size'] = 12
rcParams['figure.figsize'] = (8, 10)

##### SOLAR #####
FS = pd.read_csv('Data/DE_F_Solar.csv', delimiter=',',header=None, index_col=False)
print(FS)
FS=FS/4
# Calculate fraction of days within a 56-day rolling window for each hour of the day
# Calculate fraction of days within a 56-day rolling window for each hour of the day
window_size = 56  # Number of days in the rolling window
hourly_fraction = FS.gt(0).rolling(56).sum() / window_size
date_range = pd.date_range(start='2015-10-01', periods=1461, freq='D')
hourly_fraction['Dates'] = date_range
hourly_fraction['Dates'] = pd.to_datetime(hourly_fraction['Dates'])
# Display or use the resulting 'hourly_fraction' DataFrame
print(hourly_fraction)

y_list = [] # ostatni to X
for i, col in enumerate(hourly_fraction.columns):
    y = hourly_fraction[col]
    y_list.append(y)

# Create subplots

# Define the number of rows and columns for subplots
num_rows = 12
num_cols = 2

# Create subplots
fig, axes = plt.subplots(num_rows, num_cols, figsize=(15, 2 * num_rows))
plt.subplots_adjust(wspace=0.05)
plt.subplots_adjust(hspace=0.3)
# Flatten the axes array if there's only one row
axes = axes.flatten() if num_rows > 1 else [axes]

# Plot each column in a subplot
for i, col in enumerate(hourly_fraction.columns):
    if i < len(axes):  # Ensure i doesn't go out of bounds
        ax = axes[i]

        ax.plot(hourly_fraction['Dates'], hourly_fraction[col])

        ax.set_yticks([0, 0.25, 0.5, 0.75, 1])
        if i % num_cols == 1:
            ax.yaxis.set_ticks([])

        ax.xaxis.set_ticks([])

        # Add x ticks only on the last row
        if i >= len(axes) - num_cols:
            n_ticks = 9
            date_ticks = hourly_fraction['Dates'].iloc[::len(hourly_fraction['Dates']) // n_ticks]
            ax.set_xticks(date_ticks)
            ax.set_xticklabels(date_ticks.dt.strftime('%Y-%m-%d'), rotation=45, ha='right')

        bbox_width = ax.get_position().width

        # Draw a rectangle behind the title
        ax.set_title(f'{col}',
                     bbox=dict(facecolor='lightgrey', edgecolor='black', boxstyle='round,pad=0.3'))

# Adjust layout for better spacing
#plt.tight_layout()
plt.savefig('Plots/9 Fractions.png')
# Show the plots
plt.show()


