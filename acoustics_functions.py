import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import Funcion_sigma
# Parámetros--------------------------------------------

#Velocidad del sonido [m/s2]
c_o = 343
#Densidad del aire 
ro_o = 1.18
#Frecuencias de interés tercio octava (f_to) [Hz]
f_to = [20,25,31.5,40,50,63,80,100,125,160,200,250,315,400,500,630,800,1000,1250,1600,2000,2500,3150,4000,5000,6300,8000,10000,12500,16000,20000]
#longitud de onda [m]
lon_onda = []
for i in range(0,len(f_to)-1):
    f_i = f_to[i]
    lon_onda_i = round(c_o/f_i,2)
    lon_onda.append(lon_onda_i)


# Datos de entrada -------------------------------------

#Espesor del elemento [m]
t = 0.0125
#Densidad del material [kg/m3]
ro_m = 800
#Ancho del elemento
l_x = 6
#Alto del elemento
l_y = 4
#Modulo de Young o modulo de elasticidad
e = 2*(10**9)
#Factor de perdidas interno del elemento
n_in = 6*(10**(-3))
#Módulo de pisson del elemento
poisson = 0.24


# Calculos ---------------------------------------------

#Masa superficial del material [kg/m2]
m_s = ro_m*t
#Superficie del elemento
s = l_x*l_y
#Rigidez
b = (e*(t**3))/(12*(1-(poisson**2)))
#Frecuencia crítica
f_c = ((c_o**2)/(2*np.pi))*((m_s/b)**(1/2))
#Frecuencia densidad
f_d = (e/(2*np.pi*ro_m))*((m_s/b)**(1/2))

#Modelo de Cremer - Ley de masa--------------------------------------
def mod_cremer_fun(f_to, f_c, f_d, m_s):
    '''
    Cremer model
    '''
    r_to = []

    for i in range(len(f_to)):
        if f_to[i]<f_c:
            r = 20*np.log10(m_s*f_to[i]) - 47
            r_to.append(r)
        elif f_d>f_to[i]>f_c:
            n_tot = n_in + (m_s/(485*(f_to[i]**(1/2))))
            r_2 = 20*np.log10(m_s*f_to[i]) - 10*np.log10(np.pi/(4*n_tot)) + 10*np.log10(f_to[i]/f_c) - 10*np.log(f_c/(f_to[i]-f_c)) - 47
            r_to.append(r_2)
        else :
            r_3 = 20*np.log10(m_s*f_to[i]) - 47
            r_to.append(r_3)
    return r_to
    
    
# Modelo ISO 12354 -----------------------------------------------------

#DEJAR FUNCION MAIN EN ESTE Y DEJAR UN .py APARTE PARA LAS DEMÁS??

#Factor de radiación para ondas de flexión libres
sigma = [] #El que calculo Pablo

#Numero de onda
k_o = []
for i in range(len(f_to)):
    k_o_i = 2*np.pi*f_to[i]/c_o
    k_o.append(k_o_i)

def nabla_fun(k_o, l_x, l_y):
    '''
    nabla
    '''
    nabla = []
    for i in range(len(f_to)):
        nabla_i = -0.964 - (0.5+(l_y/(np.pi*l_x)))*np.log(l_y/l_x) + ((5*l_y)/(2*np.pi*l_x)) - (1/(4*np.pi*l_x*l_y*(k_o[i]**2)))
        nabla.append(nabla_i)
    return nabla

def sigma_f_fun(nabla, k_o, l_x, l_y):
    '''
    forced wave radiation factor
    '''
    sigma_f =[]
    for i in range(len(f_to)):
        sigma_f_i = 0.5*(np.log(k_o[i]*((l_x*l_y)**(1/2)))-nabla[i])
        if sigma_f_i > 2:
            sigma_f_i = 2    
        sigma_f.append(sigma_f_i)    
    return sigma_f

def r_to_iso_fun(sigma, sigma_f, l_x, l_y, f_to):
    '''
    Calculates the R by ISO12354
    sigma: array. free bending waves radiation factor
    sigma_f: array. forced bending waves radiation factor
    n_tot: array. total loss factor
    l_x: float. width
    l_y: float. height
    f_to: array. frecuency per third octave band
    '''


    r_to_iso = []
    for i in range(len(f_to)):
        #Factor de transmisión por banda de tercio de octavas
        tau_a = ((2*ro_o*c_o)/(2*np.pi*f_to[i]*m_s))**2
        tau_b = ((sigma[i])**2)/(n_in + (m_s/(485*((f_to[i])**(1/2)))))
        if f_to[i] > f_c:
            tau = tau_a*(tau_b*(np.pi*f_c/(2*f_to[i])))
            r_i = -10*np.log10(tau)
            r_to_iso.append(r_i)
        elif f_to[i] < f_c:
            tau = tau_a*(2*sigma_f[i] + (((l_x+l_y)**2)/(l_x**2+l_y**2))*((f_c/f_to[i])**(1/2))*tau_b)
            r_i = -10*np.log10(tau)
            r_to_iso.append(r_i)
        else:
            tau = tau_a*(tau_b*np.pi/2)
            r_i = -10*np.log10(tau)
            r_to_iso.append(r_i)
    return r_to_iso



#Ejemplo

nabla = nabla_fun(k_o, 6, 4)

sigmaf = sigma_f_fun(nabla, k_o, 6, 4)

sigma = Funcion_sigma.sigma(f_c, 6, 4)

print(f"Nabla {nabla}", f"Sigma_F {sigmaf}")

R_ISO = r_to_iso_fun(sigma,  sigmaf, 6, 4, f_to)

print(f"R_final: {R_ISO}")