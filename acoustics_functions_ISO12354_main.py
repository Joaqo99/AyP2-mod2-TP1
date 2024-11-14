import numpy as np
import Funciones_ISO
import materiales
# Parámetros--------------------------------------------

#Velocidad del sonido [m/s2]
c_o = 343
#Densidad del aire 
ro_o = 1.18
#Frecuencias de interés tercio octava (f_to) [Hz]
f_to = [20,25,31.5,40,50,63,80,100,125,160,200,250,315,400,500,630,800,1000,1250,1600,2000,2500,3150,4000,5000,6300,8000,10000,12500,16000,20000]

# Modelo ISO 12354 -----------------------------------------------------

def iso_method(material, l_x, l_y, t_m):
    """
    Calculates the sound reduction index (R) based on ISO 12354.

    Parameters:
    - material(String): Input data material.
    - sigma (array): Free bending waves radiation factor.
    - sigma_f (array): Forced bending waves radiation factor.
    - l_x (float): Width of the panel or element (meters).
    - l_y (float): Height of the panel or element (meters).
    - t_m (array): Frequencies in third-octave bands (Hz).

    Returns:
    - r_to_iso (list): Sound reduction index (R) for each frequency band in `f_to`.
    - f_c (float): The critical frequency (Hz) for the material.

    """
    #Ingreso datos
    material_props = materiales.get_material_properties(material)
    
    #Datos de material
    n_in = float(material_props["Factor de pérdidas"])
    ro_m = float(material_props["Densidad"])
    e = float(material_props["Módulo de Young"])
    poisson = float(material_props["Módulo Poisson"])
    t = t_m/1000
    m_s = ro_m*t

    
    #Parametros de otras funciones
    k_o = []
    for i in range(len(f_to)):
        k_o_i = 2*np.pi*f_to[i]/c_o
        k_o.append(k_o_i)

    lambda_m = Funciones_ISO.nabla_fun(k_o, l_x, l_y)
    sigma_f = Funciones_ISO.sigma_f_fun(lambda_m, k_o, l_x, l_y)

    #Rigidez
    b = (e*(t**3))/(12*(1-(poisson**2)))
    #Frecuencia crítica
    f_c = ((c_o**2)/(2*np.pi))*((m_s/b)**(1/2))

    sigma = Funciones_ISO.sigma(f_c, l_x, l_y)


    #Calculo de R segun ISO 12354

    r_to_iso = []

    for i in range(len(f_to)):
        #Factor de transmisión por banda de tercio de octavas
        tau_a = ((2*ro_o*c_o)/(2*np.pi*f_to[i]*m_s))**2
        tau_b = ((sigma[i])**2)/(n_in + (m_s/(485*((f_to[i])**(1/2)))))
        if f_to[i] > f_c:
            tau = tau_a*(tau_b*(np.pi*f_c/(2*f_to[i])))
            r_i = -10*np.log10(tau)
            r_to_iso.append(round(r_i,2))
        elif f_to[i] < f_c :
            tau = tau_a*(2*sigma_f[i] + (((l_x+l_y)**2)/(l_x**2+l_y**2))*((f_c/f_to[i])**(1/2))*tau_b)
            r_i = -10*np.log10(tau)
            r_to_iso.append(round(r_i,2))
        else:
            tau = tau_a*((tau_b*np.pi)/2)
            r_i = -10*np.log10(tau)
            r_to_iso.append(round(r_i,2))
            
    return f_c, r_to_iso

