import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

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

#ElementoPYL 


#Espesor del elemento [m]
t = 0.0125
#Densidad del material [kg/m3]
ro_m = 800
#Ancho del elemento
l_x = 2
#Alto del elemento
l_y = 2
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



#print(round(b,2),round(f_c,2),round(f_d,2))
"""
# Modelo Cremer ---------------------------



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
    
"""    

# Modelo Sharp ---------------------------
r_sh_to = []


for i in range(len(f_to)):
    if f_to[i] < (0.5*f_c):
        r__0 = 10 * np.log10(1+((np.pi*m_s*f_to[i])/(ro_o*c_o))**2) - 5.5
        r_sh_to.append(r__0)
    elif f_to[i] >= f_c:
        n_tot = n_in + (m_s/(485*(np.sqrt(f_to[i]))))
        r__1 = 10 * np.log10(1+((np.pi*m_s*f_to[i])/(ro_o*c_o))**2) + 10 * np.log10((2*n_tot*f_to[i])/(np.pi*f_c))
        r__2 = 10 * np.log10(1+((np.pi*m_s*f_to[i])/(ro_o*c_o))**2) - 5.5
        r_out = min(r__1,r__2)
        r_sh_to.append(r_out)
    else:
        r_sh_to.append(None)

#Encuentro las posiciones donde no hay valor y encuentro los maximos y minimos.
posiciones_none = [i for i, valor in enumerate(r_sh_to) if valor is None]

f_mid = []
r_mid = []
print(posiciones_none)
f_r_min_pos = min(posiciones_none)
f_r_max_pos = max(posiciones_none)
f_r_max_pos += 1
f_r_min_pos -= 1
print(f"POSICION: {f_r_max_pos}")

f_r_min = f_to[f_r_min_pos]
print(f_r_min)
f_r_max = f_to[f_r_max_pos]
print(f_r_max)

# Armo listas para graficar interpolación entre puntos

f_mid.append(f_r_min)
f_mid.append(f_r_max)

r_mid.append(r_sh_to[f_r_min_pos])
r_mid.append(r_sh_to[f_r_max_pos])


print(f"frecuencias del medio: {f_mid}")
print(f"frecuencias del medio: {r_mid}")

print(f"Frecuencia critica = {round(f_c,2)}",f"Frecuencia de densidad = {round(f_d,2)}",f"valores de R: {r_sh_to}")

# Datos de ejemplo
frecuencias = f_to  # Frecuencias de bandas de octava en Hz
reduccion_sonora = r_sh_to  # Valores de reducción sonora en dB

# Estilo moderno
sns.set_theme(style="whitegrid")
plt.figure(figsize=(10, 6))

# Gráfico de líneas
plt.plot(frecuencias, reduccion_sonora, marker='o', color='b', linestyle='-', linewidth=2, markersize=6, label='Reducción Sonora')

# Grafico la linea de interpolacion
plt.plot(f_mid, r_mid, marker='o', color='b', linestyle='-', linewidth=2, markersize=6, label='Reducción Sonora')

# Etiquetas y título
plt.xlabel("Frecuencia [Hz]", fontsize=14)
plt.ylabel("Reducción Sonora [dB]", fontsize=14)
plt.title("Reducción Sonora por Bandas de Octava", fontsize=16)
plt.yscale("linear")  # Cambia a 'log' si necesitas una escala logarítmica
plt.xscale("log")  # Escala logarítmica en el eje x

bandas_octava = [31.5, 63, 125, 250, 500, 1000, 2000, 4000, 8000, 16000]
plt.xticks(bandas_octava, labels=bandas_octava, rotation=45)

plt.legend()
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()

# Mostrar gráfico
plt.show()


print("Joaquín")
print("Luca")
