import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import materiales
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

#Modelo de Cremer - Ley de masa--------------------------------------

def cremer_method(material, t_m):
    """
    Calculates the critical frequency and transmission loss (R values) for a material based on
    the Cremer method, used for estimating sound insulation properties of a material.

    Parameters:
    - material (str): The name of the material (e.g., 'Concrete', 'Wood', etc.).
    
    Returns:
    - f_c (float): The critical frequency (Hz) for the material.
    - r_cremer_to (list): A list of transmission loss values (R values) at specific frequencies.
    
    """
        
    material_props = materiales.get_material_properties(material)
    
    n_in = float(material_props["Factor de pérdidas"])
    ro_m = float(material_props["Densidad"])
    e = float(material_props["Módulo de Young"])
    poisson = float(material_props["Módulo Poisson"])
    t = t_m/1000
    m_s = ro_m*t

    #Rigidez
    b = (e*(t**3))/(12*(1-(poisson**2)))
    #Frecuencia crítica
    f_c = ((c_o**2)/(2*np.pi))*((m_s/b)**(1/2))
    #Frecuencia densidad
    f_d = (e/(2*np.pi*ro_m))*((m_s/b)**(1/2))

    r_to_cremer = []

    for i in range(len(f_to)):
        n_tot = n_in + (m_s / (485 * (f_to[i] ** (1 / 2))))
        if f_to[i] < f_c:
            r = 20 * np.log10(m_s * f_to[i]) - 47
        elif f_c <= f_to[i] < f_d:
            r = (20 * np.log10(m_s * f_to[i]) - 10 * np.log10((np.pi) / (4 * n_tot)) 
                 + 10 * np.log10(f_to[i] / f_c) + 10*np.log10(1-(f_c/f_to[i])) - 47)
        else:  # Esto cubre f_to[i] >= f_d
            r = 20 * np.log10(m_s * f_to[i]) - 47
        r_to_cremer.append(round(r,2))
    return f_c, r_to_cremer