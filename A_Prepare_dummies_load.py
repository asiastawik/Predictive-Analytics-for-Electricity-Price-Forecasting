import numpy as np
import pandas as pd


dummy = pd.read_csv('Data/Dummies.csv', delimiter=',', header=None, index_col=False)
print(dummy)
new_dummy = dummy[[0, 5, 6]]
print(new_dummy)
new_dummy.to_csv('New_data/Dummies_1.csv', index=False, header=None)