from matplotlib import pyplot as plt
from matplotlib.ticker import MaxNLocator
from scipy import signal
import numpy as np

f_to = [20, 25, 31.5, 40, 50, 63, 80, 100, 125, 160, 200, 250, 315, 400, 500, 630, 800, 1000, 1250, 1600, 2000, 2500, 3150, 4000, 5000, 6300, 8000, 10000, 12500, 16000, 20000]

def plot_R(R_davy=False, R_sharp=False, R_iso=False, R_cremer=False):
    """
    Plots Transmission Loss graph
    Input:
        R_davy: array type object. R values by Davy method
        R_sharp: array type object. R values by sharp method
        R_iso: array type object. R values by iso method
        R_cremer: array type object. R values by cremer method
    """
    fig, ax = plt.subplots()
    fig.set_figheight(5)
    fig.set_figwidth(10)
    fig.tight_layout(pad=4)  # Ajusta 'pad' para el margen general
    fig.patch.set_facecolor("#4e5d6c")
    ax.set_facecolor("#152534")

    R_max = 0

    if R_davy:
        ax.semilogx(f_to, R_davy, label="Davy", color="Violet")
        R_davy_max = np.max(R_davy)
        if R_davy_max > R_max:
            R_max = R_davy_max

    if R_sharp:
        ax.semilogx(f_to, R_sharp, label="Sharp", color="Red")
        R_sharp_max = np.max(R_sharp)
        if R_sharp_max > R_max:
            R_max = R_sharp_max

    if R_iso:
        ax.semilogx(f_to, R_iso, label="ISO", color="Blue")
        R_iso_max = np.max(R_iso)
        if R_iso_max > R_max:
            R_max = R_iso_max

    if R_cremer:
        ax.semilogx(f_to, R_cremer, label="Pared Simple", color="Green")
        R_cremer_max = np.max(R_cremer)
        if R_cremer_max > R_max:
            R_max = R_cremer_max

    # Configuración de etiquetas y ejes
    ax.set_xlabel("Frecuencia [Hz]")
    ax.set_ylabel("Transmission Loss [dB]")
    ax.set_xlim(20, 21000)
    
    # Eliminamos los *ticks* por defecto y configuramos nuestros propios *ticks* con tamaño personalizado
    ax.set_xticks(f_to)
    ax.tick_params(axis='x', which='both', length=0)  # Elimina los ticks predeterminados
    ax.set_xticklabels([f'{t}' for t in f_to], rotation=45, ha='right', fontsize=8)  # Establece el tamaño de fuente
    
    ax.set_ylim(0, R_max + 10)
    ax.grid(linewidth=0.2)
    ax.legend()

    return fig, ax