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
#-----------------------------------------------------------------------------
def cenilka_beta(X,Y):
    Xt = np.array(X).transpose()
    XtX = np.matmul(Xt, X)
    inv_XtX = np.linalg.inv(XtX)
    XtY = np.matmul(Xt,Y)
    cenilka = np.matmul(inv_XtX, XtY)
    return cenilka
#-----------------------------------------------------------------------------
# cenilki za oba modela

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

print('---------------------------------------------------------------------------------------------------------')
print(f'Enostavna linearna regresija nam da številski oceni: \n'
      f'-beta_0: {round(b0_eno,4)}\n'
      f'-beta_1: {round(b1_eno,6)}')
print('---------------------------------------------------------------------------------------------------------')
print(f'Model linearne regresija, ki upošteva nihanje temperature skozi leto nam da številske ocene:\n'
      f'-beta_0: {round(b0_nihanje,6)}\n'
      f'-[beta_1, beta_2, ..., beta_12]: {b1_12_nihanje}')
print('---------------------------------------------------------------------------------------------------------')

#----------------------------------------------------------
ocena_za_jan_2040 = b0_nihanje * (2040 + 1/12) + b1_12_nihanje[0]
ocena_za_povp_2040 = b0_nihanje * (2040 + 13/24) + sum(b1_12_nihanje)/12
#----------------------------------------------------------
print(f'OCENA ZA TEMPERATURO JANUARJA 2040: {round(ocena_za_jan_2040, 4)}\n'
      f'OCENA ZA POVPREČNO TEMPERATURO 2040: {round(ocena_za_povp_2040, 4)}')
print('---------------------------------------------------------------------------------------------------------')

#--------------------------------------------------------------------
# napovedi in intervali zaupanja

m= len(Y_podatki)
p_nih = len(beta_nihanje)
p_eno = 2

Xt_nihanje = np.array(X_nihanje).transpose()
XtX_nihanje = np.matmul(Xt_nihanje, X_nihanje)
inv_XtX_nihanje = np.linalg.inv(XtX_nihanje)

X_beta_nihanje = np.matmul(X_nihanje, beta_nihanje)
vekt_nih = [(Y_podatki[i] - X_beta_nihanje[i]) for i in range(m)]

sigma_plus_nih = np.linalg.norm(vekt_nih)/(math.sqrt(m - p_nih))

inv_st5_407 = 1.96581
inv_st1_407 = 2.58796

c1 = [2040+1/12, 1] + [0 for _ in range(11)]
c1T = np.array(c1).transpose()
c1T_beta = np.matmul(c1T, beta_nihanje)
sep_plus_c1 = sigma_plus_nih * math.sqrt(1 + np.matmul(np.matmul(c1T, inv_XtX_nihanje), c1))

int_jan_5_levo = c1T_beta - inv_st5_407 * sep_plus_c1
int_jan_5_desno = c1T_beta + inv_st5_407 * sep_plus_c1

int_jan_1_levo = c1T_beta - inv_st1_407 * sep_plus_c1
int_jan_1_desno = c1T_beta + inv_st1_407 * sep_plus_c1

cc = [2040 + 13/24] + [1/12 for _ in range(12)]
ccT = np.array(cc).transpose()
ccT_beta = np.matmul(ccT, beta_nihanje)
sep_plus_cc = sigma_plus_nih * math.sqrt(1 + np.matmul(np.matmul(c1T, inv_XtX_nihanje), c1))

int_povp_5_levo = ccT_beta - inv_st5_407 * sep_plus_cc
int_povp_5_desno = ccT_beta + inv_st5_407 * sep_plus_cc

int_povp_1_levo = ccT_beta - inv_st1_407 * sep_plus_cc
int_povp_1_desno = ccT_beta + inv_st1_407 * sep_plus_cc

#------------------------------------------------------------------------------------------
print(f'Interval zaupanja za oceno temperature jan 2024 je:\n'
      f'-pri alfa = 0.05: [{round(int_jan_5_levo,4)}, {round(int_jan_5_desno,4)}]\n'
      f'-pri alfa = 0.01: [{round(int_jan_1_levo,4)}, {round(int_jan_1_desno,4)}]')
print('---------------------------------------------------------------------------------------------------------')


print(f'Interval zaupanja za oceno povprečne temperature leta 2024 je:\n'
      f'-pri alfa = 0.05: [{round(int_povp_5_levo,4)}, {round(int_povp_5_desno,4)}]\n'
      f'-pri alfa = 0.01: [{round(int_povp_1_levo,4)}, {round(int_povp_1_desno,4)}]')
print('---------------------------------------------------------------------------------------------------------')

#-----------------------------------------------------------------------------
# p-vrednosti in statistična značilnost

Xt_eno = np.array(X_eno).transpose()
XtX_eno = np.matmul(Xt_eno, X_eno)
inv_XtX_eno = np.linalg.inv(XtX_eno)

X_beta_eno = np.matmul(X_eno, beta_eno)
vekt_eno = [(Y_podatki[i] - X_beta_eno[i]) for i in range(m)]

sigma_plus_eno = np.linalg.norm(vekt_eno)/(math.sqrt(m - p_eno))

c1_eno = [0,1]
c1T_eno = np.array(c1_eno).transpose()
c1T_beta_eno = np.matmul(c1T_eno, beta_eno)
sep_plus_c1_eno = sigma_plus_eno * math.sqrt(np.matmul(np.matmul(c1T_eno, inv_XtX_eno), c1_eno))


cc_nih_p = [1] + [0 for _ in range(12)]
ccT_nih_p = np.array(cc_nih_p).transpose()
ccT_beta_nih_p = np.matmul(ccT_nih_p, beta_nihanje)
sep_plus_cc_nih_p = sigma_plus_nih * math.sqrt(np.matmul(np.matmul(ccT_nih_p, inv_XtX_nihanje), cc_nih_p))

nast_za_p_vrednost_eno = b1_eno/sep_plus_c1_eno
nast_za_p_vrednost_nih  = b0_nihanje/sep_plus_cc_nih_p

pomoc_p_vredn_nih = 0.9999999999999911668434
pomoc_p_vredn_eno = 0.9689
p_vrednost_eno = 2*(1 - pomoc_p_vredn_eno)
p_vrednost_nih = 2*(1 - pomoc_p_vredn_nih)

print(f'P-VREDNOSTI:\n'
      f'-pri preizkusu povezanim z enostavno regresijom je argument za Student(418): {round(nast_za_p_vrednost_eno, 8)},  '
      f'p-vrednost bo torej: {round(p_vrednost_eno, 6)}\n'
      f'-pri preizkusu povezanim z upoštevanim nihanjem temperature je argument za Student(407): {round(nast_za_p_vrednost_nih, 8)},  '
      f'p-vrednost bo torej: {p_vrednost_nih}.')
print('---------------------------------------------------------------------------------------------------------')

inv_st5_418 = 1.96566
print(f'Vrednost koeficienta D, ki določa test, ki spoštuje standardno stopnjo tveganja je: {round(inv_st5_418 * sep_plus_c1_eno, 4)}.')
print('---------------------------------------------------------------------------------------------------------')