import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams
import numpy as np

# initial parameters of plots
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Times New Roman']
rcParams['font.size'] = 12
rcParams['figure.figsize'] = (15, 4)

##### DAY AHEAD #####

DA = pd.read_csv('Data/BZN_DayAhead.csv', delimiter=',',header=None, index_col=False)
DA_4am = DA[:][4]
DA_6pm = DA[:][18]
# Plot
plt.figure(1)
plt.plot(DA_4am, label='off-peak (4 AM)')
plt.plot(DA_6pm, label='peak (6 PM)')
plt.xticks(np.arange(0,1461,step=365),['10.2015', '10.2016', '10.2017', '10.2018', '10.2019'])
plt.yticks(np.arange(-100,201,step=100), ["-100", "0", "100", "200"])
plt.legend()
plt.title("Day-ahead")
plt.xlabel("Date")
plt.ylabel("Price [EUR/MWh]")
plt.grid()
plt.savefig('Plots/1 Day-ahead')
plt.show()

##### INTRADAY #####

ID = pd.read_csv('Data/Intraday.csv', delimiter=',',header=None, index_col=False)
ID_4am = ID[:][4]
ID_6pm = ID[:][18]
# Plot
plt.figure(2)
plt.plot(ID_4am, label='off-peak (4 AM)')
plt.plot(ID_6pm, label='peak (6 PM)')
plt.xticks(np.arange(0,1461,step=365),['10.2015', '10.2016', '10.2017', '10.2018', '10.2019'])
plt.yticks(np.arange(-100,201,step=100), ["-100", "0", "100", "200"])
plt.legend()
plt.title("Intraday")
plt.xlabel("Date")
plt.ylabel("Price [EUR/MWh]")
plt.grid()
plt.savefig('Plots/2 Intraday')
plt.show()

##### LOAD #####

L = pd.read_csv('Data/DE_Load.csv', delimiter=',',header=None, index_col=False)
FL = pd.read_csv('Data/DE_F_Load.csv', delimiter=',',header=None, index_col=False)
L['Average'] = L.mean(axis=1)
FL['Average'] = FL.mean(axis=1)
# Podzielone przez 4 ?!
L=L/4
FL=FL/4
# Plot
plt.figure(3)
plt.plot(L['Average'])
plt.xticks(np.arange(0,1461,step=365),['10.2015', '10.2016', '10.2017', '10.2018', '10.2019'])
plt.title("Load")
plt.xlabel("Date")
plt.ylabel("Load [GWh]")
plt.grid()
plt.savefig('Plots/3 Load')
plt.show()
# Errors
errors_load = FL['Average'] - L['Average']
# Plot
plt.figure(4)
plt.plot(errors_load)
plt.xticks(np.arange(0,1461,step=365),['10.2015', '10.2016', '10.2017', '10.2018', '10.2019'])
plt.title("Errors Load")
plt.ylabel("Errors [GWh]")
plt.xlabel("Date")
plt.grid()
plt.savefig('Plots/4 Errors Load')
plt.show()

##### WIND #####
W = pd.read_csv('Data/DE_Wind.csv', delimiter=',',header=None, index_col=False)
FW = pd.read_csv('Data/DE_F_Wind.csv', delimiter=',',header=None, index_col=False)
W['Average'] = W.mean(axis=1)
FW['Average'] = FW.mean(axis=1)
# Podzielone przez 4 ?!
W=W/4
FW=FW/4
# Plot
plt.figure(5)
plt.plot(W['Average'])
plt.xticks(np.arange(0,1461,step=365),['10.2015', '10.2016', '10.2017', '10.2018', '10.2019'])
plt.title("Wind")
plt.xlabel("Date")
plt.ylabel("Generation [GWh]")
plt.grid()
plt.savefig('Plots/5 Wind')
plt.show()
# Errors
errors_wind = FW['Average'] - W['Average']
# Plot
plt.figure(6)
plt.plot(errors_wind)
plt.xticks(np.arange(0,1461,step=365),['10.2015', '10.2016', '10.2017', '10.2018', '10.2019'])
plt.title("Errors Wind")
plt.ylabel("Errors [GWh]")
plt.xlabel("Date")
plt.grid()
plt.savefig('Plots/6 Errors Wind')
plt.show()

##### SOLAR #####
S = pd.read_csv('Data/DE_Solar.csv', delimiter=',',header=None, index_col=False)
FS = pd.read_csv('Data/DE_F_Solar.csv', delimiter=',',header=None, index_col=False)
S['Average'] = S.mean(axis=1)
FS['Average'] = FS.mean(axis=1)
# Podzielone przez 4 ?!
S=S/4
FS=FS/4
# Plot
plt.figure(7)
plt.plot(S['Average'])
plt.xticks(np.arange(0,1461,step=365),['10.2015', '10.2016', '10.2017', '10.2018', '10.2019'])
plt.title("Solar")
plt.xlabel("Date")
plt.ylabel("Generation [GWh]")
plt.grid()
plt.savefig('Plots/7 Solar')
plt.show()
# Errors
errors_solar = FS['Average'] - S['Average']
# Plot
plt.figure(8)
plt.plot(errors_solar)
plt.xticks(np.arange(0,1461,step=365),['10.2015', '10.2016', '10.2017', '10.2018', '10.2019'])
plt.title("Errors Solar")
plt.ylabel("Errors [GWh]")
plt.xlabel("Date")
plt.grid()
plt.savefig('Plots/8 Errors Solar')
plt.show()