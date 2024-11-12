import numpy as np
import Sigma_Davy
import Shear_Davy

def Single_leaf_Davy(frequency, density, Young, Poisson, thickness, lossfactor, length, width):
    # Definición de constantes
    po = 1.18          # Densidad del aire [kg/m^3]
    c0 = 343           # Velocidad del sonido [m/s]
    cos21Max = 0.9     # Ángulo límite definido en el trabajo de Davy
    
    # Cálculos iniciales
    surface_density = density * thickness
    critical_frequency = np.sqrt(12 * density * (1 - Poisson ** 2) / Young) * c0 ** 2 / (2 * thickness * np.pi)
    normal = po * c0 / (np.pi * frequency * surface_density)
    normal2 = normal ** 2
    e = 2 * length * width / (length + width)
    cos2l = c0 / (2 * np.pi * frequency * e)
    
    # Limitar cos2l según cos21Max
    if cos2l > cos21Max:
        cos2l = cos21Max
    
    # Cálculo de tau1
    tau1 = normal2 * np.log((normal2 + 1) / (normal2 + cos2l))
    
    # Cálculo de ratio y r
    ratio = frequency / critical_frequency
    r = 1 - 1 / ratio
    if r < 0:
        r = 0
    
    # Cálculo de G, rad, netatotal, z, y, y tau2
    G = np.sqrt(r)
    rad = Sigma_Davy.Sigma(G, frequency, length, width)  
    rad2 = rad ** 2
    netatotal = lossfactor + rad * normal
    z = 2 / netatotal
    y = np.arctan(z) - np.arctan(z * (1 - ratio))
    tau2 = normal2 * rad2 * y / (netatotal * 2 * ratio)
    tau2 *= Shear_Davy.shear(frequency, density, Young, Poisson, thickness)  
    
    # Condición para calcular tau
    if frequency < critical_frequency:
        tau = tau1 + tau2
    else:
        tau = tau2
    
    # Resultado final
    single_leaf = -10 * np.log10(tau)
    return single_leaf