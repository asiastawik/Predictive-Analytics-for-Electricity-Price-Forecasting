from matplotlib import rcParams
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# initial parameters of plots
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Times New Roman']
rcParams['font.size'] = 12
rcParams['figure.figsize'] = (15, 4)


def load_data(file_path):
    data = pd.read_csv(file_path, delimiter=',', header=None, index_col=False)
    return data


df = load_data('New_data/Forecast_load_enhanced_2016.csv')
df['Average'] = df.mean(axis=1)
plt.plot(df['Average'])
plt.xlabel('Dates')
plt.xticks(np.arange(0, len(df['Average']), step=30), ['10.2016', '11.2016', '12.2016', '01.2017', '02.2017', '03.2017',
                                                       '04.2017', '05.2017', '06.2017', '07.2017', '08.2017', '09.2017',
                                                       '10.2017'])
plt.ylabel('Load')
plt.title('Average forecast 2016')
plt.show()
