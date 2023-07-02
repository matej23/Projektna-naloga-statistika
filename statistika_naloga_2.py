import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import math

kromatin_kratki = pd.read_csv('Kromatin_kratki.csv', names = ['DOLZINA'], header=None)
kromatin_srednji = pd.read_csv('Kromatin_srednji.csv', names = ['DOLZINA'], header=None)
kromatin_dolgi = pd.read_csv('Kromatin_dolgi.csv', names = ['DOLZINA'],  header=None)

#zapisimo cenilki, ki smo jo teoreticno ze poracunali
def cenilka_mnv(podatki):
    theta = 0
    for i in range(len(podatki.DOLZINA)):
        theta += (podatki.DOLZINA[i])**2
    cenilka = math.sqrt(theta/(2*len(podatki.DOLZINA)))
    return cenilka

def cenilka_mm(podatki):
    theta = 0
    for i in range(len(podatki.DOLZINA)):
        theta += podatki.DOLZINA[i]
    cenilka = math.sqrt(2/math.pi) * theta/(len(podatki.DOLZINA))
    return cenilka

theta_mnv_kratki = cenilka_mnv(kromatin_kratki)
theta_mnv_srednji = cenilka_mnv(kromatin_srednji)
theta_mnv_dolgi = cenilka_mnv(kromatin_dolgi)

theta_mm_kratki = cenilka_mm(kromatin_kratki)
theta_mm_srednji = cenilka_mm(kromatin_srednji)
theta_mm_dolgi = cenilka_mm(kromatin_dolgi)
 

#------------------------------------------------------------------------------

def gostota(x, theta):
    if x <= 0:
        print('pazi')
        return 0
    else:
        vrednost = x/(theta**2) * math.e**(-(x**2)/(2*(theta**2)))
        return vrednost 


def verjetje(theta, podatki):
    produkt = 1
    for i in range(len(podatki.DOLZINA)):
        produkt = produkt * gostota(podatki.DOLZINA[i], theta)
    return produkt

theta = np.linspace(1/2, 4, 1000)
vrednost_verjetja_kratki = verjetje(theta, kromatin_kratki)
vrednost_verjetja_srednji = verjetje(theta, kromatin_srednji)
vrednost_verjetja_dolgi = verjetje(theta, kromatin_dolgi)

fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10,7)) 
fig.suptitle('VERJETJA ZA RAZLIČNE VRSTE KROMATINA')
fig.tight_layout(pad=2.0)

ax1.yaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.25)
ax1.set(axisbelow=True, title= 'Verjetje za kratek Kromatin', ylabel='Verjetje')

ax2.yaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.25)
ax2.set(axisbelow=True, title= 'Verjetje za srednji Kromatin', ylabel='Verjetje')

ax3.yaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.25)
ax3.set(axisbelow=True, title= 'Verjetje za dolgi Kromatin', ylabel='Verjetje')

ax1.plot(theta, vrednost_verjetja_kratki, color='r')
ax2.plot(theta, vrednost_verjetja_srednji, color='g')
ax3.plot(theta, vrednost_verjetja_dolgi, color='b')

ax1.plot([theta_mnv_kratki, theta_mnv_kratki], [0, verjetje(theta_mnv_kratki, kromatin_kratki)], linestyle='--', color="#FF9E9E")
ax1.plot(theta_mnv_kratki, verjetje(theta_mnv_kratki, kromatin_kratki), marker='o', color="black")

ax2.plot([theta_mnv_srednji, theta_mnv_srednji], [0, verjetje(theta_mnv_srednji, kromatin_srednji)], linestyle='--', color="#92F799")
ax2.plot(theta_mnv_srednji, verjetje(theta_mnv_srednji, kromatin_srednji), marker="o", color="black")

ax3.plot([theta_mnv_dolgi, theta_mnv_dolgi], [0, verjetje(theta_mnv_dolgi, kromatin_dolgi)], linestyle='--', color="#7AB4FF")
ax3.plot(theta_mnv_dolgi, verjetje(theta_mnv_dolgi, kromatin_dolgi), marker="o", color="black")


plt.show()
