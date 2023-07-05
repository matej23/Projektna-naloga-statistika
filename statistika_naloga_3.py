import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import math

oznake = ['LETO', 'MESEC', 'TEMPERATURA']
temperature = pd.read_csv('Temp_LJ.csv', names=oznake, header=0)

Y_podatki = temperature.TEMPERATURA
leta = temperature.LETO
meseci = temperature.MESEC

X_eno = [[1, leta[i] + meseci[i]/12] for i in range(len(Y_podatki))]
X_nihanje = [([leta[i]+ meseci[i]/12] + [1 if meseci[i] == j else 0 for j in range(1, 13)]) for i in range(len(Y_podatki))]
"""
X_nihanje_pomozni = [([leta[i]+ meseci[i]/12] + [[1, leta[i] + meseci[i]/12] if meseci[i] == j else [0,0] for j in range(1, 13)]) for i in range(len(Y_podatki))]
X_nihanje_neuspelo = []
for i in range(len(X_nihanje_pomozni)):
    vrstica_i = [X_nihanje_pomozni[i][0]]
    for j in range(1, len(X_nihanje_pomozni[i])):
        vrstica_i += X_nihanje_pomozni[i][j]
    X_nihanje_neuspelo.append(vrstica_i)
"""
#-----------------------------------------------------------------------------
def cenilka_beta(X,Y):
    Xt = np.array(X).transpose()
    XtX = np.matmul(Xt, X)
    inv_XtX = np.linalg.inv(XtX)
    XtY = np.matmul(Xt,Y)
    cenilka = np.matmul(inv_XtX, XtY)
    return cenilka
#-----------------------------------------------------------------------------
beta_eno = cenilka_beta(X_eno, Y_podatki)
b0_eno = beta_eno[0]
b1_eno = beta_eno[1]

beta_nihanje = cenilka_beta(X_nihanje, Y_podatki)
b0_nihanje = beta_nihanje[0]
b1_12_nihanje = beta_nihanje[1:]

interval = np.linspace(1986, 35 + 1986, 1000)
premica_eno_lin_reg = b0_eno + interval * b1_eno

fig, ax = plt.subplots()

X_graf = [[leta[i] + meseci[i]/12] for i in range(len(Y_podatki))]

ax.plot(interval, premica_eno_lin_reg, c ='#CC0066')
ax.legend(['Linearen trend spreminjanja temperature skozi leta, zaznan z enostavno linearno regresijo'])
ax.scatter(X_graf, Y_podatki, c ="#3399FF", marker ='.')

ax.yaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.25)
ax.set(axisbelow=True, title="PODATKI O POVPREČNIH MESEČNIH TEMPERATURAH SKOZI LETA", ylabel='Temperatura', xlabel = 'Leto')

#plt.show()

('---------------------------------------------------------------------------------------------------------')
print(f'Enostavna linearna regresija nam da številski oceni: \n'
      f'-beta_0: {round(b0_eno,4)}\n'
      f'-beta_1: {round(b1_eno,6)}')
print('---------------------------------------------------------------------------------------------------------')
print(f'Model linearne regresija, ki upoštevanje nihanje temperature skozi leti nam da številske ocene:\n'
      f'-beta_0: {round(b0_nihanje,6)}\n'
      f'-[beta_1, beta_2, ..., beta_12]: {b1_12_nihanje}')
print('---------------------------------------------------------------------------------------------------------')
