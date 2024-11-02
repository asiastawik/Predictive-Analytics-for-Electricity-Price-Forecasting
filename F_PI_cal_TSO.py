import pandas as pd

Y_TSO_1 = pd.read_csv('New_data/Y_Intraday1_TSO.csv', delimiter=',',header=None, index_col=False)
#print((Y_TSO_1))

#ID_TSO_1 = pd.read_csv('New_data/Forecast_Intraday1_TSO.csv', delimiter=',',header=None, index_col=False)
#print((ID_TSO_1))

#DA_TSO_1 = pd.read_csv('New_data/Forecast_DayAhead_TSO.csv', delimiter=',',header=None, index_col=False)
#print((DA_TSO_1[0][0]))

#real
ID_TSO = pd.read_csv('Data/Intraday.csv', delimiter=',',header=None, index_col=False)
DA_TSO = pd.read_csv('Data/BZN_DayAhead.csv', delimiter=',',header=None, index_col=False)

ID_list = []
ID_list.extend(ID_TSO.values.flatten())
ID_TSO = ID_list[731*24:(731+365)*24]
print(len(ID_TSO))
DA_list = []
DA_list.extend(DA_TSO.values.flatten())
DA_TSO = DA_list[731*24:(731+365)*24]
print(len(DA_TSO))
lista_pi_1 =[]

Y_TSO_1 = Y_TSO_1[0:365*24]
print(len(Y_TSO_1))
for element in range(len(Y_TSO_1)):
    lista_pi_1.append(Y_TSO_1[0][element]*ID_TSO[element]+(1-Y_TSO_1[0][element])*DA_TSO[element]-DA_TSO[element])

sum_of_elements = sum(lista_pi_1)

print("Intraday TSO 1:", sum_of_elements)


Y_TSO_2 = pd.read_csv('New_data/Y_Intraday2_TSO.csv', delimiter=',',header=None, index_col=False)
#print((Y_TSO_1))
Y_TSO_2 = Y_TSO_2[0:365*24]
print(len(Y_TSO_2))
lista_pi_2 =[]

for element in range(len(Y_TSO_2)):
    lista_pi_2.append(Y_TSO_2[0][element]*ID_TSO[element]+(1-Y_TSO_2[0][element])*DA_TSO[element]-DA_TSO[element])

sum_of_elements2 = sum(lista_pi_2)

print("Intraday TSO 2:", sum_of_elements2)


Y_TSO_3 = pd.read_csv('New_data/Y_Intraday3_TSO.csv', delimiter=',',header=None, index_col=False)
Y_TSO_3=Y_TSO_3[0:365*24]
print(len(Y_TSO_3))
lista_pi_3 =[]

for element in range(len(Y_TSO_3)):
    lista_pi_3.append(Y_TSO_3[0][element]*ID_TSO[element]+(1-Y_TSO_3[0][element])*DA_TSO[element]-DA_TSO[element])

sum_of_elements3 = sum(lista_pi_3)

print("Intraday TSO 3:", sum_of_elements3)