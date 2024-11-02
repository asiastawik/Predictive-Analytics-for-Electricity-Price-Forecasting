import pandas as pd
### REAL ###
##### DAY AHEAD #####

DA = pd.read_csv('Data/BZN_DayAhead.csv', delimiter=',',header=None, index_col=False)
DA_list = []
DA_list.extend(DA.values.flatten())

##### INTRA DAY  #####
ID = pd.read_csv('Data/Intraday.csv', delimiter=',',header=None, index_col=False)
ID_list = []
ID_list.extend(ID.values.flatten())
y_list=[]
for element in range(len(ID_list)):
    if ID_list[element]>DA_list[element]:
        y_list.append(1)
    else:
        y_list.append(0)


### REAL ###
##### DAY AHEAD #####  <2017-2018>

DA_TSO = pd.read_csv('New_data/Forecast_dayAhead_real_2017_2018.csv', delimiter=',',header=None, index_col=False)
DA_TSO_list = []
DA_TSO_list.extend(DA_TSO.values.flatten())

##### INTRA DAY1  #####  <2017-2018>
ID1_TSO = pd.read_csv('New_data/Forecast_Intraday_Real.csv', delimiter=',',header=None, index_col=False)
ID1_TSO_list = []
ID1_TSO_list.extend(ID1_TSO.values.flatten())
y1_list=[]
for element in range(len(ID1_TSO_list)):
    if ID1_TSO_list[element]>DA_TSO_list[element]:
        y1_list.append(1)
    else:
        y1_list.append(0)

y_list_2017_2018 = y_list[731*24:(731+365)*24]
p1 = 0
for element in range(365*24):
    if y_list_2017_2018[element] == y1_list[element]:
        p1 += 1
result1 = p1/(365*24)
print('INTRADAY REAL 1')
print(result1)
#
returning = pd.DataFrame({'Final': y1_list})
returning.to_csv('New_data/Y_Intraday1_Real.csv', index=False, header = None)

##### INTRA DAY2  #####  <2017-2018>
ID2_TSO = pd.read_csv('New_data/Forecast_Intraday2_Real.csv', delimiter=',',header=None, index_col=False)
ID2_TSO_list = []
ID2_TSO_list.extend(ID2_TSO.values.flatten())
y2_list=[]
for element in range(len(ID2_TSO_list)):
    if ID2_TSO_list[element]>DA_TSO_list[element]:
        y2_list.append(1)
    else:
        y2_list.append(0)

p2 = 0
y2_list = y2_list[:365*24]
for element in range(365*24):
    if y_list_2017_2018[element] == y2_list[element]:
        p2 += 1
result2 = p2/(365*24)
print('INTRADAY REAL 2')
print(result2)
#
returning2 = pd.DataFrame({'Final': y2_list})
returning2.to_csv('New_data/Y_Intraday2_Real.csv', index=False, header = None)

##### INTRA DAY3  #####  <2017>
ID3_TSO = pd.read_csv('New_data/Forecast_Intraday3_Real.csv', delimiter=',',header=None, index_col=False)
ID3_TSO_list = []
ID3_TSO_list.extend(ID3_TSO.values.flatten())
y3_list=[]
for element in range(len(ID3_TSO_list)):
    if ID3_TSO_list[element]>DA_TSO_list[element]:
        y3_list.append(1)
    else:
        y3_list.append(0)
y_list_2017 = y_list[731*24:(731+365)*24]
p3 = 0
for element in range(365*24):
    if y_list_2017[element] == y3_list[element]:
        p3 += 1
result3 = p3/(365*24)
print('INTRADAY REAL 3')
print(result3)
#
returning3 = pd.DataFrame({'Final': y3_list})
returning3.to_csv('New_data/Y_Intraday3_Real.csv', index=False, header = None)

import matplotlib.pyplot as plt
plt.plot(ID_list[(731*24):((731+365+365)*24)], label='ID')
plt.plot(ID1_TSO_list, label='ID 1 TSO')
plt.plot(ID2_TSO_list, label='ID 2 TSO')
plt.plot(ID3_TSO_list, label='ID 3 TSO')
plt.legend()
plt.show()


