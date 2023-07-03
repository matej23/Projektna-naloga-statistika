import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import math

oznake = ['LETO', 'MESEC', 'TEMPERATURA']
temperature = pd.read_csv('Temp_LJ.csv', names=oznake, header=0)

Y = temperature.TEMPERATURA
leta = temperature.LETO
meseci = temperature.MESEC
X = []
for i in range(len(Y)):
    X.append(leta[i] + meseci[i]/12 - 1986)

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

def cenilka_b0(X,Y):
    cenilka = ((sum_xi2(X) * sum(Y)) - (sum(X) * sum_xiyi(X, Y)))/((len(X)*sum_xi2(X)) - (sum(X)**2))
    return cenilka

def cenilka_b1(X,Y):
    cenilka = ((len(X) * sum_xiyi(X, Y)) - (sum(X) * sum(Y)))/((len(X)*sum_xi2(X)) - (sum(X)**2))
    return cenilka

b0_eno = cenilka_b0(X, Y)
b1_eno = cenilka_b1(X, Y)

print(b0_eno, b1_eno)

interval = np.linspace(0, 35, 1000)
premica_eno_lin_reg = b0_eno + interval * b1_eno

#-----------------------------------------------------------------------------

Y_delitev_po_letih = [temperature[temperature.LETO == i].TEMPERATURA for i in range(1986,2021)]
Y_povprecne = [np.mean(Y_delitev_po_letih[i]) for i in range(len(Y_delitev_po_letih))]

X_za_povprecne = [[1]+[i + j*1/12 for j in range(12)] for i in range(35)]
X_leta = [i for i in range(35)]
#print(np.linalg.inv(A))
#np.matmul(a, b)
#a.transpose()
def cenilka_beta(X,Y):
    Xt = np.array(X).transpose()
    XtX = np.matmul(Xt, X)
    inv_XtX = np.linalg.inv(XtX)
    XtY = np.matmul(Xt,Y)
    cenilka = np.matmul(inv_XtX, XtY)
    return cenilka

#beta_povp = cenilka_beta(X_za_povprecne, Y_povprecne) 
b0_povp = cenilka_b0(X_leta, Y_povprecne)
b1_povp = cenilka_b1(X_leta, Y_povprecne)
print(b0_povp, b1_povp)
#------------------------------------------------------------------------------
fig, ax = plt.subplots()

# We need to draw the canvas, otherwise the labels won't be positioned and 
# won't have values yet.
fig.canvas.draw()

ax.plot(interval, premica_eno_lin_reg, c ='r')
ax.scatter(X, Y, c ="blue")

labels = [f'{1986 + 5*(i-1)}' for i in range(9)]
ax.set_xticklabels(labels)

#plt.show()

