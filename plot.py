from matplotlib import pyplot as plt
import numpy as np

f_to = [20, 25, 31.5, 40, 50, 63, 80, 100, 125, 160, 200, 250, 315, 400, 500, 630, 800, 1000, 1250, 1600, 2000, 2500, 3150, 4000, 5000, 6300, 8000, 10000, 12500, 16000, 20000]

def initialize_plot():
    fig, ax = plt.subplots()
    fig.set_figheight(5)
    fig.set_figwidth(10)
    fig.tight_layout(pad=4)
    fig.patch.set_facecolor("#4e5d6c")
    ax.set_facecolor("#152534")
    
    # Crear líneas para cada método (vacías inicialmente)
    line_davy, = ax.semilogx([], [], label="Davy", color="Violet")
    line_sharp, = ax.semilogx([], [], label="Sharp", color="Red")
    line_iso, = ax.semilogx([], [], label="ISO 12354-1", color="Blue")
    line_cremer, = ax.semilogx([], [], label="Pared Simple", color="Green")

    ax.set_xlabel("Frecuencia [Hz]")
    ax.set_ylabel("Transmission Loss [dB]")
    ax.set_ylim(0, 100)
    ax.set_xlim(20, 20000)
    ax.set_xticks(f_to)
    ax.set_xticklabels([f'{t}' for t in f_to], rotation=45, ha='right', fontsize=8)
    ax.grid(linewidth=0.2)
    
    # Retornar la figura, los ejes y las líneas
    return fig, ax, {"R_davy": line_davy, "R_sharp": line_sharp, "R_iso": line_iso, "R_cremer": line_cremer}

def add_critical_frequency(ax, f_c):
    # Borrar la línea de frecuencia crítica existente si la hay
    for line in ax.get_lines():
        if "Frecuencia Crítica" in line.get_label():
            line.remove()
    
    f_c_label = f"Frecuencia Crítica: {np.round(f_c, 1)} Hz"
    # Dibujar una nueva línea en la frecuencia crítica
    critical_line = ax.axvline(x=f_c, color="#aaa", linestyle="--", label=f_c_label)
    
    # Actualizar la leyenda para mostrar solo líneas con datos
    update_legend(ax)
    ax.figure.canvas.draw()

def update_legend(ax):
    # Mostrar solo las líneas con datos en la leyenda
    lines_with_data = [line for line in ax.get_lines() if len(line.get_data()[0]) > 0]
    labels_with_data = [line.get_label() for line in lines_with_data]
    ax.legend(lines_with_data, labels_with_data)

def update_plot(lines, R_values, f_c=None):
    # Actualizar los datos de cada línea según los valores de R disponibles
    for key, line in lines.items():
        if R_values[key] is not None:
            line.set_data(f_to, R_values[key])
        else:
            line.set_data([], [])
    
    # Ajustar el eje Y para que muestre el rango adecuado
    all_values = [v for v in R_values.values() if v is not None]
    if all_values:
        R_max = max(np.max(v) for v in all_values)
        lines["R_davy"].axes.set_ylim(0, R_max + 10) 
    
    # Actualizar la leyenda solo para las líneas que tienen datos
    ax = list(lines.values())[0].axes
    update_legend(ax)

    # Agregar la línea de frecuencia crítica si se proporciona
    if f_c is not None:
        add_critical_frequency(ax, f_c)

def clear_plot(lines):
    # Borrar los datos de cada línea
    for line in lines.values():
        line.set_data([], [])

    # Eliminar la leyenda actual si existe
    ax = list(lines.values())[0].axes
    if ax.get_legend() is not None:
        ax.get_legend().remove()
    ax.set_ylim(0, 100)

    # Borrar la línea de frecuencia crítica si existe
    for line in ax.get_lines():
        if "Frecuencia Crítica" in line.get_label():
            line.remove()
    
    # Redibujar el gráfico sin datos y sin leyenda
    ax.figure.canvas.draw()