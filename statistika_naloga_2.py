import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import math

kromatin_kratki = pd.read_csv('Kromatin_kratki.csv', names = ['DOLZINA'], header=None)
kromatin_srednji = pd.read_csv('Kromatin_srednji.csv', names = ['DOLZINA'], header=None)
kromatin_dolgi = pd.read_csv('Kromatin_dolgi.csv', names = ['DOLZINA'],  header=None)

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

se_mm_kratki = math.sqrt((4 - math.pi)/(math.pi * len(kromatin_kratki.DOLZINA)) * (theta_mm_kratki**2))
se_mm_srednji = math.sqrt((4 - math.pi)/(math.pi * len(kromatin_srednji.DOLZINA)) * (theta_mm_srednji**2))
se_mm_dolgi = math.sqrt((4 - math.pi)/(math.pi * len(kromatin_dolgi.DOLZINA)) * (theta_mm_dolgi**2))

se_mnv_kratki = math.sqrt((theta_mm_kratki**2)/(4 * len(kromatin_kratki.DOLZINA)))
se_mnv_srednji = math.sqrt((theta_mm_srednji**2)/(4 * len(kromatin_srednji.DOLZINA)))
se_mnv_dolgi = math.sqrt((theta_mm_dolgi**2)/(4 * len(kromatin_dolgi.DOLZINA)))

#------------------------------------------------------------------------------

def gostota(x, theta):
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

fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10,10)) 
fig.suptitle('VERJETJA ZA RAZLIČNE VRSTE KROMATINA', fontsize=14)
fig.tight_layout(pad=3.0)

ax1.yaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.25)
ax1.set(axisbelow=True, ylabel='Verjetje', xlabel = "Vrednost parametra")

ax2.yaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.25)
ax2.set(axisbelow=True, ylabel='Verjetje', xlabel = "Vrednost parametra")

ax3.yaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.25)
ax3.set(axisbelow=True, ylabel='Verjetje', xlabel = "Vrednost parametra")

ax1.plot(theta, vrednost_verjetja_kratki, color='r')
ax1.legend(['Verjetje za kratek Kromatin'])
ax2.plot(theta, vrednost_verjetja_srednji, color='g')
ax2.legend(['Verjetje za srednji Kromatin'])
ax3.plot(theta, vrednost_verjetja_dolgi, color='b')
ax3.legend(['Verjetje za dolgi Kromatin'])

ax1.plot([theta_mnv_kratki, theta_mnv_kratki], [0, verjetje(theta_mnv_kratki, kromatin_kratki)], linestyle='--', color="#FF9E9E")
ax1.plot(theta_mnv_kratki, verjetje(theta_mnv_kratki, kromatin_kratki), marker='o', color="black")
ax1.plot([theta_mnv_kratki - se_mnv_kratki, theta_mnv_kratki + se_mnv_kratki], [1* 10**(-40), 1 * 10**(-40)], linestyle='--', color="#FF9E9E")
ax1.plot(theta_mnv_kratki- se_mnv_kratki, 1 * 10**(-40), marker="|", color="#FF9E9E")
ax1.plot(theta_mnv_kratki+ se_mnv_kratki, 1 * 10**(-40), marker="|", color="#FF9E9E")

int_kratki = np.linspace(theta_mnv_kratki - se_mnv_kratki, theta_mnv_kratki + se_mnv_kratki,1000)
ax1.fill_between(int_kratki, 3.4*10**(-40), color='#FF9E9E', alpha=0.3)

ax2.plot([theta_mnv_srednji, theta_mnv_srednji], [0, verjetje(theta_mnv_srednji, kromatin_srednji)], linestyle='--', color="#A6E681")
ax2.plot(theta_mnv_srednji, verjetje(theta_mnv_srednji, kromatin_srednji), marker="o", color="black")
ax2.plot([theta_mnv_srednji - se_mnv_srednji, theta_mnv_srednji + se_mnv_srednji], [2* 10**(-184), 2 * 10**(-184)], linestyle='--', color="#A6E681")
ax2.plot(theta_mnv_srednji- se_mnv_srednji, 2 * 10**(-184), marker="|", color="#A6E681")
ax2.plot(theta_mnv_srednji+ se_mnv_srednji, 2 * 10**(-184), marker="|", color="#A6E681")

int_srednji = np.linspace(theta_mnv_srednji - se_mnv_srednji, theta_mnv_srednji + se_mnv_srednji, 1000)
ax2.fill_between(int_srednji, 9.3*10**(-184), color='#92F799', alpha=0.2)

ax3.plot([theta_mnv_dolgi, theta_mnv_dolgi], [0, verjetje(theta_mnv_dolgi, kromatin_dolgi)], linestyle='--', color="#7AB4FF")
ax3.plot(theta_mnv_dolgi, verjetje(theta_mnv_dolgi, kromatin_dolgi), marker="o", color="black")
ax3.plot([theta_mnv_dolgi - se_mnv_dolgi, theta_mnv_dolgi + se_mnv_dolgi], [1/4 * 10**(-119), 1/4 * 10**(-119)], linestyle='--', color="#7AB4FF")
ax3.plot(theta_mnv_dolgi - se_mnv_dolgi, 1/4 * 10**(-119), marker="|", color="#7AB4FF")
ax3.plot(theta_mnv_dolgi + se_mnv_dolgi, 1/4 * 10**(-119), marker="|", color="#7AB4FF")

int_dolgi = np.linspace(theta_mnv_dolgi - se_mnv_dolgi, theta_mnv_dolgi + se_mnv_dolgi, 1000)
ax3.fill_between(int_dolgi, 1.2*10**(-119), color='#7AB4FF', alpha=0.3)
#---------------------------------------------------------------------------------------------------------------------

print('-----------------------------------------------------------------------------')
print(f'KRATKI KROMATIN:\n -vrednost cenilke po metodi momentov znaša: {round(theta_mm_kratki,4)}'
      f'\n -vrednost cenilke po metodi največjega verjetja znaša: {round(theta_mnv_kratki,4)}'
      f'\n -ocena za standardno napako po metodi momentov znaša: {round(se_mm_kratki, 6)}'
      f'\n -ocena za standardno napako po metodi največjega verjetja znaša: {round(se_mnv_kratki, 6)}')
print('\n')
print(f'SREDNJI KROMATIN:\n -vrednost cenilke po metodi momentov znaša: {round(theta_mm_srednji,4)}'
      f'\n -vrednost cenilke po metodi največjega verjetja znaša: {round(theta_mnv_srednji,4)}'
      f'\n -ocena za standardno napako po metodi momentov znaša: {round(se_mm_srednji, 6)}'
      f'\n -ocena za standardno napako po metodi največjega verjetja znaša: {round(se_mnv_srednji, 6)}')
print('\n')
print(f'DOLGI KROMATIN:\n -vrednost cenilke po metodi momentov znaša: {round(theta_mm_dolgi, 4)}'
      f'\n -vrednost cenilke po metodi največjega verjetja znaša: {round(theta_mnv_dolgi, 4)}'
      f'\n -ocena za standardno napako po metodi momentov znaša: {round(se_mm_dolgi, 6)}'
      f'\n -ocena za standardno napako po metodi največjega verjetja znaša: {round(se_mnv_dolgi, 6)}')
print('-----------------------------------------------------------------------------')

#plt.show()

#---------------------------------------------------------------------------------------------------------------
iqr_kratki = np.diff(np.quantile(kromatin_kratki, q=[.25, .75]))[0]
iqr_srednji = np.diff(np.quantile(kromatin_srednji, q=[.25, .75]))[0]
iqr_dolgi = np.diff(np.quantile(kromatin_dolgi, q=[.25, .75]))[0]

n_kratki = len(kromatin_kratki.DOLZINA)
n_srednji = len(kromatin_srednji.DOLZINA)
n_dolgi = len(kromatin_dolgi.DOLZINA)

freedman_diaconis_kratki = 2.6 * iqr_kratki/(np.cbrt(n_kratki))
freedman_diaconis_srednji =  2.6 * iqr_srednji/(np.cbrt(n_srednji))
freedman_diaconis_dolgi = 2.6 * iqr_dolgi/(np.cbrt(n_dolgi))

def number_of_bins(fd, podatki):
    podatki_min, podatki_max = podatki.DOLZINA.min(), podatki.DOLZINA.max()
    podatki_range = podatki_max - podatki_min
    stevilo = round(podatki_range/fd)
    return stevilo

n_bins_kratki = number_of_bins(freedman_diaconis_kratki, kromatin_kratki)
n_bins_srednji = number_of_bins(freedman_diaconis_srednji, kromatin_srednji)
n_bins_dolgi = number_of_bins(freedman_diaconis_dolgi, kromatin_dolgi)

max_kratki = kromatin_kratki.DOLZINA.max()
max_srednji = kromatin_srednji.DOLZINA.max()
max_dolgi = kromatin_dolgi.DOLZINA.max()

int_gostota_kratki = np.linspace(0, max_kratki + 1/5, 1000)
int_gostota_srednji = np.linspace(0, max_srednji + 1/3, 1000)
int_gostota_dolgi = np.linspace(0, max_dolgi + 1/2, 1000)

gostota_kratki_mm = gostota(int_gostota_kratki, theta_mm_kratki) * len(kromatin_kratki.DOLZINA) * freedman_diaconis_kratki
gostota_kratki_mnv = gostota(int_gostota_kratki, theta_mnv_kratki) * len(kromatin_kratki.DOLZINA) * freedman_diaconis_kratki
gostota_srednji_mm = gostota(int_gostota_srednji, theta_mm_srednji) * len(kromatin_srednji.DOLZINA) * freedman_diaconis_srednji
gostota_srednji_mnv = gostota(int_gostota_srednji, theta_mnv_srednji) * len(kromatin_srednji.DOLZINA) * freedman_diaconis_srednji
gostota_dolgi_mm = gostota(int_gostota_dolgi, theta_mm_dolgi) * len(kromatin_dolgi.DOLZINA) * freedman_diaconis_dolgi
gostota_dolgi_mnv = gostota(int_gostota_dolgi, theta_mnv_dolgi) * len(kromatin_dolgi.DOLZINA) * freedman_diaconis_dolgi

print(f'ŠIRINE IN ŠTEVILO BLOKOV PO MODIFICIRANEM FREEDMAN-DIACONISOVEM PRAVILU:\n'
      f'-kratek Kromatin: širina: {round(freedman_diaconis_kratki,4)}, število blokov: {n_bins_kratki}\n'
      f'-srednji Kromatin: širina: {round(freedman_diaconis_srednji,4)}, število blokov: {n_bins_srednji}\n'
      f'-dolgi Kromatin: širina: {round(freedman_diaconis_dolgi,4)}, število blokov: {n_bins_dolgi}')
print('-----------------------------------------------------------------------------')

#--------------------------------------------------------------------------------------------------------

figh, (axh1, axh2, axh3) = plt.subplots(3, 1, figsize=(10,12)) 
figh.suptitle('MERITVE ZA RAZLIČNE VRSTE KROMATINA', fontsize=14)
figh.tight_layout(pad=3.5)

axh1.plot(int_gostota_kratki, gostota_kratki_mm, color='r', linestyle = '-.')
axh1.plot(int_gostota_kratki, gostota_kratki_mnv, color='r')
axh2.plot(int_gostota_srednji, gostota_srednji_mm, color='g', linestyle = '-.')
axh2.plot(int_gostota_srednji, gostota_srednji_mnv, color='g')
axh3.plot(int_gostota_dolgi, gostota_dolgi_mm, color='b', linestyle = '-.')
axh3.plot(int_gostota_dolgi, gostota_dolgi_mnv, color='b')

axh1.legend(['Gostota, ocenjena po metodi momentov', 'Gostota, ocenjena po metodi največjega verjetja'])
axh2.legend(['Gostota, ocenjena po metodi momentov', 'Gostota, ocenjena po metodi največjega verjetja'])
axh3.legend(['Gostota, ocenjena po metodi momentov', 'Gostota, ocenjena po metodi največjega verjetja'])

axh1.hist(kromatin_kratki, n_bins_kratki, color='#FF9E9E', alpha = 0.3, edgecolor="black", linewidth=1.1)
axh1.set_title("Meritve za kratki Kromatin", loc = "right")
axh1.set_ylabel("Pojavitve")
axh1.set_xlabel("Dolžina Kromatina")

axh2.hist(kromatin_srednji, n_bins_srednji, color='#92F799',alpha = 0.3, edgecolor="black", linewidth=1.1)
axh2.set_title("Meritve za srednji Kromatin", loc = "right")
axh2.set_ylabel("Pojavitve")
axh2.set_xlabel("Dolžina Kromatina")

axh3.hist(kromatin_dolgi, n_bins_dolgi, color='#7AB4FF', alpha = 0.3, edgecolor="black", linewidth=1.1)
axh3.set_title("Meritve za dolgi Kromatin", loc = "right")
axh3.set_ylabel("Pojavitve")
axh3.set_xlabel("Dolžina Kromatina")

plt.show()