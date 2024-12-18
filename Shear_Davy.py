import numpy as np

def shear(frequency, density, Young, Poisson, thickness):
    """
    Calculates the shear factor used in the calculation of the transmission loss of a material
    based on its frequency, density, Young's modulus, Poisson's ratio, and thickness.

    Parameters:
    - frequency (float): The frequency of the incident sound wave in Hz.
    - density (float): The density of the material in kg/m^3.
    - Young (float): Young's modulus of the material in Pascals (Pa).
    - Poisson (float): Poisson's ratio of the material (dimensionless).
    - thickness (float): The thickness of the material in meters (m).

    Returns:
    - out (float): The shear factor, which is a dimensionless value used in the calculation of transmission loss.
    """
    
    # Definición de constantes
    omega = 2 * np.pi * frequency
    chi = (1 + Poisson) / (0.87 + 1.12 * Poisson)
    chi = chi ** 2
    X = thickness ** 2 / 12
    QP = Young / (1 - Poisson ** 2)
    C = -omega ** 2

    # Cálculos intermedios
    B = C * (1 + 2 * chi / (1 - Poisson)) * X
    A = X * QP / density
    kbcor2 = (-B + np.sqrt(B ** 2 - 4 * A * C)) / (2 * A)
    kb2 = np.sqrt(-C / A)

    G = Young / (2 * (1 + Poisson))
    kT2 = -C * density * chi / G
    kL2 = -C * density / QP
    kS2 = kT2 + kL2

    # Cálculo de ASI, BSI y CSI
    ASI = 1 + X * (kbcor2 * kT2 / kL2 - kT2)
    ASI = ASI ** 2
    BSI = 1 - X * kT2 + kbcor2 * kS2 / (kb2 ** 2)
    CSI = np.sqrt(1 - X * kT2 + kS2 ** 2 / (4 * kb2 ** 2))

    # Resultado final
    out = ASI / (BSI * CSI)
    return out