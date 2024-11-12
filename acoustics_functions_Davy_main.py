import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import Single_leaf_Davy
import materiales


# Datos de entrada
filtro = [20, 25, 31.5, 40, 50, 63, 80, 100, 125, 160, 200, 250, 315, 400, 500, 
          630, 800, 1000, 1250, 1600, 2000, 2500, 3150, 4000, 5000, 6300, 8000, 
          10000, 12500, 16000, 20000]

c_o = 343
ro_o = 1.18


def davy_method(material, l_y, l_x, espesor):
    """
    Calculates TL by Davy Method. 
    Input:
        material: str type object. Material name.
        espesor: float type object. Wall lenght.
        l_y: float type object. Wall height.
        l_x: float type object. Wall width.

    Output:
        Fc: float value. Returns Fc frecuency.
        R: float value. Returns TL list value.
    """
    t = espesor/1000    #paso el espesor de mm a m
    averages = 3 # Número de promedios
    dB = 0.236
    octave = 3
    material_props = materiales.get_material_properties(material)

    ro_m = int(material_props["Densidad"])
    e = float(material_props["Módulo de Young"])
    n_in = float(material_props["Factor de pérdidas"])
    poisson = float(material_props["Módulo Poisson"])


    m_s = ro_m*t
    s = l_x*l_y

    # Cálculos de rigidez a la flexión y frecuencia crítica
    B = (e / (1 - poisson ** 2)) * (t ** 3 / 12)
    Fc = (c_o ** 2 / (2 * np.pi)) * np.sqrt(m_s / B)

    # Inicialización del arreglo de resultados
    R = []

    # Bucle principal
    for f in filtro:
        Ntot = n_in + (m_s / (485 * np.sqrt(f)))
        ratio = f / Fc
        limit = 2 ** (1 / (2 * octave))

        if ratio < 1 / limit or ratio > limit:
            TLost = Single_leaf_Davy.Single_leaf_Davy(f, ro_m, e, poisson, t, Ntot, l_y, l_x)
        else:
            Avsingle_leaf = 0
            for j in range(1, averages + 1):
                factor = 2 ** ((2 * j - 1 - averages) / (2 * averages * octave))
                aux = 10 ** (-Single_leaf_Davy.Single_leaf_Davy(f * factor, ro_m, e, poisson, t, Ntot, l_y, l_x) / 10)
                Avsingle_leaf += aux
            TLost = -10 * np.log10(Avsingle_leaf / averages)

        R.append(TLost)

    # Resultado final
    R = np.array(R)
    return Fc, R


#------------------------------------------------------------------------------------------------------------------------
f_c, R = davy_method("PYL",6,4,12.5)
print(f"Reduccion sonora: {R}")

# Datos de ejemplo
frecuencias = filtro  # Frecuencias de bandas de octava en Hz
reduccion_sonora = R  # Valores de reducción sonora en dB

# Estilo moderno
sns.set_theme(style="whitegrid")
plt.figure(figsize=(10, 6))

# Gráfico de líneas
plt.plot(frecuencias, reduccion_sonora, marker='o', color='b', linestyle='-', linewidth=2, markersize=6, label='Reducción Sonora')

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
