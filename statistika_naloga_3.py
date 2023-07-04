import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import math

oznake = ['LETO', 'MESEC', 'TEMPERATURA']
temperature = pd.read_csv('Temp_LJ.csv', names=oznake, header=0)

Y_podatki = temperature.TEMPERATURA
leta = temperature.LETO
meseci = temperature.MESEC

X_eno = [[1, leta[i] + meseci[i]/12 - 1986] for i in range(len(Y_podatki))]
X_nihanje = [[1, leta[i] - 1986, meseci[i]] for i in range(len(Y_podatki))]

def sum_xi2(X):
    vsota = 0
    for i in range(len(X)):
        vsota += X[i]**2
    return vsota

def sum_xiyi(X, Y):
    vsota = 0
    for i in range(len(X)):
        vsota += X[i]*Y[i]
    return vsota

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
b0_nih = beta_nihanje[0]
b1_nih = beta_nihanje[1]
b2_nih = beta_nihanje[2]

interval = np.linspace(0, 35, 1000)
premica_eno_lin_reg = b0_eno + interval * b1_eno

fig, ax = plt.subplots()

# We need to draw the canvas, otherwise the labels won't be positioned and 
# won't have values yet.
fig.canvas.draw()


X_graf = [[leta[i] + meseci[i]/12 - 1986] for i in range(len(Y_podatki))]

ax.plot(interval, premica_eno_lin_reg, c ='r')
ax.scatter(X_graf, Y_podatki, c ="blue")

#labels = [f'{1986 + 5*(i-1)}' for i in range(9)]
#ax.set_xticklabels(labels)

#plt.show()

