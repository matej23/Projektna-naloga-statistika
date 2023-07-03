import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import math

oznake_podatkov = ['TIP','CLANOV','OTROK','DOHODEK','CETRT','IZOBRAZBA']
podatki = pd.read_csv('Kibergrad.csv', names=oznake_podatkov, header=0)

#---------------------------------------------------------------------------------------------------
# naloga 1 a)

tip_druzine1 = podatki[podatki.TIP == 1]
tip_druzine2 = podatki[podatki.TIP == 2]
tip_druzine3 = podatki[podatki.TIP == 3]

print('---------------------------------------------------------------------------------------------------------')
print(f'Imamo {len(tip_druzine1)} podatkov od družin tipa 1, {len(tip_druzine2)} podatkov od družin tipa 2 in {len(tip_druzine3)} podatkov od družin tipa 3.')
print('---------------------------------------------------------------------------------------------------------')
velikost_vzorca = 500

eno_vz_za_doh_tip1 = tip_druzine1.sample(velikost_vzorca, replace = False, random_state=9).DOHODEK
eno_vz_za_doh_tip2 = tip_druzine2.sample(velikost_vzorca, replace = False, random_state=9).DOHODEK
eno_vz_za_doh_tip3 = tip_druzine3.sample(velikost_vzorca, replace = False, random_state=9).DOHODEK

vsi_vzorci = [eno_vz_za_doh_tip1, eno_vz_za_doh_tip2, eno_vz_za_doh_tip3]

fig1 = plt.figure(figsize =(10, 7))

ax1 = fig1.add_subplot(111)

bp1 = ax1.boxplot(vsi_vzorci, patch_artist = True)
 
colors1 = ['#A4C5FF', '#FF9F9F','#95F785']
 
for patch, color in zip(bp1['boxes'], colors1):
    patch.set_facecolor(color)


for whisker in bp1['whiskers']:
    whisker.set(color ='#404040', linewidth = 1, linestyle ="--")

for cap in bp1['caps']:
    cap.set(color ='#404040', linewidth = 2.5)

colors_medians1 = ['#24478f', '#AB0000', '#138E00']

for median, color_median in zip(bp1['medians'], colors_medians1):
    median.set(color = color_median, linewidth = 3)
 
for flier in bp1['fliers']:
    flier.set(marker ='.', color ='#e7298a', alpha = 0.8)
     
ax1.set_xticklabels(['Družina z zakonskima ali \n zunajzakonskima partnerjema', 'Enostarševska družina z očetom','Enostarševska družina z materjo'])
ax1.yaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.25)
ax1.set(axisbelow=True, title="DOHODKI GLEDE NA TIP DRUŽINE", ylabel='Dohodek')

#plt.show()

#----------------------------------------------------------------------------------------------
# naloga 1 b)

doh_tip1_eno1 = tip_druzine1.sample(velikost_vzorca, replace = False, random_state=9).DOHODEK
doh_tip1_eno2 = tip_druzine1.sample(velikost_vzorca, replace = False, random_state=10).DOHODEK
doh_tip1_eno3 = tip_druzine1.sample(velikost_vzorca, replace = False, random_state=11).DOHODEK
doh_tip1_eno4 = tip_druzine1.sample(velikost_vzorca, replace = False, random_state=12).DOHODEK
doh_tip1_eno5 = tip_druzine1.sample(velikost_vzorca, replace = False, random_state=13).DOHODEK

vsa_en_vz_tip1 = [doh_tip1_eno1, doh_tip1_eno2, doh_tip1_eno3, doh_tip1_eno4, doh_tip1_eno5]

fig2 = plt.figure(figsize =(10, 7))

ax2 = fig2.add_subplot(111)

bp2 = ax2.boxplot(vsa_en_vz_tip1, patch_artist = True)
 
colors2 = ['#A4C5FF', '#CCE5FF','#CCE5FF', '#CCE5FF', '#CCE5FF']
 
for patch, color in zip(bp2['boxes'], colors2):
    patch.set_facecolor(color)

for whisker in bp2['whiskers']:
    whisker.set(color ='#404040', linewidth = 1, linestyle ="--")

for cap in bp2['caps']:
    cap.set(color ='#404040', linewidth = 2.5)

colors_medians = ['#24478f', '#24478f', '#24478f', '#24478f', '#24478f']

for median, color_median in zip(bp2['medians'], colors_medians):
    median.set(color = color_median,linewidth = 3)
 
for flier in bp2['fliers']:
    flier.set(marker ='.', color ='#e7298a', alpha = 0.8)
     
ax2.yaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.25)
ax2.set(axisbelow=True, title="DOHODKI DRUŽIN Z DVEMA PARTNERJEMA (PRI RAZLIČNIH ENOSTAVNIH VZORČENJIH)", ylabel='Dohodek')

#plt.show()

#---------------------------------------------------------------------------------------------------------------------------
# naloga 1 c)
n = len(podatki)
n1 = len(tip_druzine1)
n2 = len(tip_druzine2)
n3 = len(tip_druzine3)

w1 = n1/n
w2 = n2/n
w3 = n3/n

mu1 = np.mean(tip_druzine1.DOHODEK)
mu2 = np.mean(tip_druzine2.DOHODEK)
mu3 = np.mean(tip_druzine3.DOHODEK)


mu = w1 * mu1 + w2 * mu2 + w3 * mu3

var1 = np.var(tip_druzine1.DOHODEK)
var2 = np.var(tip_druzine2.DOHODEK)
var3 = np.var(tip_druzine3.DOHODEK)

pojasnjena_var = w1 * (mu1 - mu)**2 + w2 * (mu2 - mu)**2 + w3 * (mu3 - mu)**2
nepojasnjena_var = w1 * var1 + w2 * var2 + w3 * var3

skupna_varianca = pojasnjena_var + nepojasnjena_var

delez_pojasnjene_variance = pojasnjena_var/skupna_varianca

pojasnjen_standardni_odklon = math.sqrt(pojasnjena_var)

('---------------------------------------------------------------------------------------------------------')
print(f'Povprečna vrednost za tip družine 1: {round(mu1,2)}.')
print(f'Povprečna vrednost za tip družine 2: {round(mu2,2)}.')
print(f'Povprečna vrednost za tip družine 3: {round(mu3,2)}.')
print('---------------------------------------------------------------------------------------------------------')
print(f'S tipom družine pojasnjena varianca znaša: {round(pojasnjena_var, 2)}.')
print(f'Nepojasnjena varianca znaša: {round(nepojasnjena_var, 2)}.')
print(f'Delež pojasnjene varinace znaša: {round(delez_pojasnjene_variance, 6)}.')
print(f'Pojasnjeni standardni odklon dohodka glede na tip družine znaša: {round(pojasnjen_standardni_odklon, 2)}.')
print('---------------------------------------------------------------------------------------------------------')