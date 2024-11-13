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





def sharp_method(material, l_y, l_x, espesor):
    """
    Calculates the critical frequency and transmission loss (R values) for a material based on
    the Sharp method, used for estimating sound insulation properties of a material.

    Parameters:
    - material (str): The name of the material (e.g., 'Concrete', 'Wood', etc.).
    - l_y (float): The length of the material element in the y direction (meters).
    - l_x (float): The length of the material element in the x direction (meters).
    - espesor (float): The thickness of the material in millimeters.

    Returns:
    - f_c (float): The critical frequency (Hz) for the material.
    - r_sh_to (list): A list of transmission loss values (R values) at specific frequencies.
    
    """
    
    t = espesor/1000    #paso el espesor de mm a m

    material_props = materiales.get_material_properties(material)


    ro_m = int(material_props["Densidad"])
    e = float(material_props["Módulo de Young"])
    n_in = float(material_props["Factor de pérdidas"])
    poisson = float(material_props["Módulo Poisson"])


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

    r_sh_to = []
    
    # Calcula r_05fc y r_fc para la interpolación
    r_05fc = 10 * np.log10(1 + ((np.pi * m_s * 0.5 * f_c) / (ro_o * c_o)) ** 2) - 5.5
    
    n_tot_fc = n_in + (m_s / (485 * (np.sqrt(f_c))))
    r_1_fc = 10 * np.log10(1 + ((np.pi * m_s * f_c) / (ro_o * c_o)) ** 2) + 10 * np.log10((2 * n_tot_fc * f_c) / (np.pi * f_c))
    r_2_fc = 10 * np.log10(1 + ((np.pi * m_s * f_c) / (ro_o * c_o)) ** 2) - 5.5
    r_fc = min(r_1_fc, r_2_fc)


    print(f"FC={f_c}")
    for i in range(len(f_to)):
        if f_to[i] < (0.5*f_c):
            r_0 = 10 * np.log10(1+((np.pi*m_s*f_to[i])/(ro_o*c_o))**2) - 5.5
            r_sh_to.append(r_0)
        elif f_to[i] >= f_c:
            n_tot = n_in + (m_s/(485*(np.sqrt(f_to[i]))))
            r_1 = 10 * np.log10(1+((np.pi*m_s*f_to[i])/(ro_o*c_o))**2) + 10 * np.log10((2*n_tot*f_to[i])/(np.pi*f_c))
            r_2 = 10 * np.log10(1+((np.pi*m_s*f_to[i])/(ro_o*c_o))**2) - 5.5
            r_out = min(r_1,r_2)
            r_sh_to.append(r_out)
        else:
            
            # Interpolación lineal entre r_05fc y r_fc
            r_values = r_05fc + ((r_fc - r_05fc) / (f_c - 0.5*f_c)) * (f_to[i] - f_c * 0.5)
            r_sh_to.append(r_values)
  


    print("valores R1 (fc/2): ", r_05fc)
    print("valores R2 (fc): ", r_fc)

    return f_c, r_sh_to

