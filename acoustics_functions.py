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

#Espesor del elemento [m]
t = 0.05
#Densidad del material [kg/m3]
ro_m = 2660
#Ancho del elemento
l_x = 2
#Alto del elemento
l_y = 2
#Modulo de Young o modulo de elasticidad
e = 16*(10**9)
#Factor de perdidas interno del elemento
n_in = 2*(10**(-2))
#Módulo de pisson del elemento
poisson = 0.15


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
    
    

print(f_to[i],round(f_c,2),round(f_d,2),n_in, n_tot, r_2, r_to)

# Datos de ejemplo
frecuencias = f_to  # Frecuencias de bandas de octava en Hz
reduccion_sonora = r_to  # Valores de reducción sonora en dB

# Estilo moderno
sns.set_theme(style="whitegrid")
plt.figure(figsize=(10, 6))

# Gráfico de líneas
plt.plot(frecuencias, reduccion_sonora, marker='o', color='b', linestyle='-', linewidth=2, markersize=6, label='Reducción Sonora')

# Etiquetas y título
plt.xlabel("Frecuencia (Hz)", fontsize=14)
plt.ylabel("Reducción Sonora (dB)", fontsize=14)
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

print("Luca")
print("Apellido")
print("Prueba de Branch")