import numpy as np

def Sigma(G, freq, width, length):
    """
    Calculates the radiation efficiency of a panel using a formula based on the frequency,
    panel dimensions, and a given parameter G. The function uses a series of intermediate 
    calculations to estimate the radiation efficiency of the panel in relation to the sound 
    frequency.

    Parameters:
    - G (float): A derived parameter related to the transmission loss and frequency.
    - freq (float): The frequency of the incident sound wave in Hz.
    - width (float): The width of the panel in meters (m).
    - length (float): The length of the panel in meters (m).

    Returns:
    - rad (float): The radiation efficiency of the panel (dimensionless).
    """
    
    # Definición de constantes
    c0 = 343           # Velocidad del sonido [m/s]
    w = 1.3
    beta = 0.234
    n = 2

    # Cálculos iniciales
    S = length * width
    U = 2 * (length + width)
    twoa = 4 * S / U
    k = 2 * np.pi * freq / c0
    f = w * np.sqrt(np.pi / (k * twoa))
    
    # Limitar f a un máximo de 1
    if f > 1:
        f = 1

    h = 1 / (np.sqrt(k * twoa / np.pi) * 2 / 3 - beta)
    q = 2 * np.pi / (k ** 2 * S)
    qn = q ** n

    # Cálculo de xn en función de G y f
    if G < f:
        alpha = h / f - 1
        xn = (h - alpha * G) ** n
    else:
        xn = G ** n

    # Resultado final
    rad = (xn + qn) ** (-1 / n)
    return rad