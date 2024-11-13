import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import materiales
import plot
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

from acoustics_functions_Sharp import sharp_method
from acoustics_functions_Davy_main import davy_method


# Ventana principal
window = ttk.Window(themename="superhero")
window.title("Transmission Loss Calculator")
window.geometry("1400x900")

R_values = {
    "R_sharp": None,
    "R_davy": None,
    "R_iso": None,
    "R_cremer": None
}

f_c = None

canvas = None

# Segmentación de contenedores
window.rowconfigure(0, weight=1)  # Menús
window.rowconfigure(1, weight=20) # Gráficos

# Columnas de menús
window.columnconfigure(0, minsize=700, weight=2)  
window.columnconfigure(1, minsize=400, weight=5)  
window.columnconfigure(2, minsize=300, weight=2)  

####################
# Menú opciones
options_frame = ttk.Labelframe(window, text="Opciones")
options_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=5)

frame_superior = ttk.Frame(options_frame)
frame_superior.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

frame_inferior = ttk.Frame(options_frame)
frame_inferior.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

# Menubutton para selección de materiales

def seleccion_material(x):
    pass

selected_material = ttk.StringVar()
largo_var = ttk.StringVar()
ancho_var = ttk.StringVar()
espesor_var = ttk.StringVar()

selected_material.set("Material")
materiales_menu_button = ttk.Menubutton(frame_superior, textvariable=selected_material)
materiales_menu_button.grid(row=0, column=0, columnspan=2 , padx=5, pady=5)

# Crear menú y agregar opciones
materiales_menu = ttk.Menu(materiales_menu_button, tearoff=0)
materiales_menu_button["menu"] = materiales_menu

# Lista de materiales
materials_list = materiales.get_materials_list()
for mat in materials_list:
    materiales_menu.add_radiobutton(label=mat, variable=selected_material, command=lambda mat=mat: seleccion_material(mat), value=mat)



dimensiones_label = ttk.Label(frame_inferior, text="Dimensiones:", font="-weight bold")
dimensiones_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

largo_label = ttk.Label(frame_inferior, text="Largo [m]:")
largo_label.grid(row=0, column=1, padx=5, pady=5, sticky="e")
largo_entry = ttk.Entry(frame_inferior, width=5)
largo_entry.grid(row=0, column=2, padx=5, pady=5, sticky="w")

alto_label = ttk.Label(frame_inferior, text="Alto [m]:")
alto_label.grid(row=0, column=3, padx=5, pady=5, sticky="e")
alto_entry = ttk.Entry(frame_inferior, width=5)
alto_entry.grid(row=0, column=4, padx=5, pady=5, sticky="w")

espesor_label = ttk.Label(frame_inferior, text="Espesor [mm]:")
espesor_label.grid(row=0, column=5, padx=5, pady=5, sticky="e")
espesor_entry = ttk.Entry(frame_inferior, width=5)
espesor_entry.grid(row=0, column=6, padx=5, pady=5, sticky="w")

######################
# Menú funciones
functions_frame = ttk.Labelframe(window, text="Funciones")
functions_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=5)

functions_frame.columnconfigure(0, weight=1)
functions_frame.columnconfigure(1, weight=1)
functions_frame.rowconfigure(0, weight=1)
functions_frame.rowconfigure(1, weight=1)



def procesar():
    global canvas, R_values
    material = selected_material.get()
    largo = float(largo_entry.get())
    alto = float(alto_entry.get())
    espesor = float(espesor_entry.get())

    if sharp.get():
        f_c, R_values["R_sharp"] = sharp_method(material, alto, largo, espesor)
    else:
        R_values["R_sharp"] = None
    
    if davy.get():
        f_c, R_values["R_davy"] = davy_method(material, alto, largo, espesor)
    else:
        R_values["R_davy"] = None

    # Actualizar los datos de las líneas sin recrear el gráfico
    plot.update_plot(lines, R_values, f_c)  # Pasamos las líneas y los nuevos valores de R
    canvas.draw()

    #hacer control de errores si no hay nada seleccionado


boton_procesar = ttk.Button(functions_frame, text="Procesar", bootstyle=PRIMARY, padding=3, width=14, command=procesar)
boton_procesar.grid(row=0, column=0, padx=5, pady=5)


#agregar material
def nuevo_material():

    def agregar_material():
        nombre = nombre_entry.get()
        densidad = den_entry.get()
        ym = ym_entry.get()
        lf = lf_entry.get()
        pm = pm_entry.get()

        new_mat_dict = {"Name": nombre,
               "Den": densidad,
               "YM": ym,
               "LF": lf,
               "PM": pm,
               }
        
        materiales.add_material(new_mat_dict)
        add_mat_win.destroy()

    # Crear ventana emergente
    add_mat_win = ttk.Toplevel(window)
    add_mat_win.title("Agregar Material")
    add_mat_win.geometry("500x400")
    
    # Etiquetas y campos de entrada para el nuevo material
    nombre_label = ttk.Label(add_mat_win, text="Nombre del Material:")
    nombre_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
    nombre_entry = ttk.Entry(add_mat_win, width=20)
    nombre_entry.grid(row=0, column=1, padx=10, pady=10)
    
    den_label = ttk.Label(add_mat_win, text="Densidad:")
    den_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
    den_entry = ttk.Entry(add_mat_win, width=20)
    den_entry.grid(row=1, column=1, padx=10, pady=10)
    
    ym_label = ttk.Label(add_mat_win, text="Modulo de Young:")
    ym_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")
    ym_entry = ttk.Entry(add_mat_win, width=20)
    ym_entry.grid(row=2, column=1, padx=10, pady=10)

    lf_label = ttk.Label(add_mat_win, text="Factor de perdidas:")
    lf_label.grid(row=3, column=0, padx=10, pady=10, sticky="w")
    lf_entry = ttk.Entry(add_mat_win, width=20)
    lf_entry.grid(row=3, column=1, padx=10, pady=10)

    pm_label = ttk.Label(add_mat_win, text="Moudlo de Poisson:")
    pm_label.grid(row=4, column=0, padx=10, pady=10, sticky="w")
    pm_entry = ttk.Entry(add_mat_win, width=20)
    pm_entry.grid(row=4, column=1, padx=10, pady=10)
    
    # Botón para confirmar la adición del material
    confirmar_button = ttk.Button(add_mat_win, text="Agregar", bootstyle=SUCCESS, command=agregar_material)
    confirmar_button.grid(row=5, column=0, columnspan=2, pady=10)
    

boton_agregar_material = ttk.Button(functions_frame, text="Agregar Material", bootstyle=SECONDARY, padding=3, width=14, command=nuevo_material)
boton_agregar_material.grid(row=0, column=1, padx=5, pady=5)

#exportar
boton_exportar = ttk.Button(functions_frame, text="Exportar", bootstyle=SECONDARY, padding=3, width=14)
boton_exportar.grid(row=1, column=0, padx=5, pady=5)

#borrar

def borrar():
    # Llamar a la función clear_plot para borrar las líneas del gráfico
    plot.clear_plot(lines)
    
    # Limpiar las entradas de largo, alto y espesor
    largo_entry.delete(0, "end")
    alto_entry.delete(0, "end")
    espesor_entry.delete(0, "end")
    selected_material.set("Material")

    # Actualizar el gráfico
    canvas.draw()

boton_borrar = ttk.Button(functions_frame, text="Borrar", bootstyle=DANGER, padding=3, width=14, command=borrar)
boton_borrar.grid(row=1, column=1, padx=5, pady=5)

###########################
# Menú de métodos de cálculo
davy = ttk.IntVar()
cremer = ttk.IntVar()
sharp = ttk.IntVar()
iso = ttk.IntVar()

methods_frame = ttk.Labelframe(window, text="Métodos de cálculo")
methods_frame.grid(row=0, column=2, sticky="nsew", padx=10, pady=5)

methods_frame.columnconfigure(0, weight=1)
methods_frame.columnconfigure(1, weight=1)
methods_frame.rowconfigure(0, weight=1)
methods_frame.rowconfigure(1, weight=1)

davy_check = ttk.Checkbutton(methods_frame, text="Davy", variable=davy)
pared_simple_check = ttk.Checkbutton(methods_frame, text="Pared Simple", variable=cremer)
sharp_check = ttk.Checkbutton(methods_frame, text="Sharp", variable=sharp)
iso_check = ttk.Checkbutton(methods_frame, text="ISO", variable=iso)

davy_check.grid(row=0, column=0, sticky="w", padx=5, pady=5)
pared_simple_check.grid(row=0, column=1, sticky="w", padx=5, pady=5)
sharp_check.grid(row=1, column=0, sticky="w", padx=5, pady=5)
iso_check.grid(row=1, column=1, sticky="w", padx=5, pady=5)

# Frame para el gráfico
graph_frame = ttk.Frame(window, bootstyle="secondary")
graph_frame.grid(row=1, column=0, columnspan=3, sticky="nsew", padx=10, pady=5)

# Inicializar gráfico y curvas
graph_fig, ax, lines = plot.initialize_plot()  # Creamos el gráfico sin datos
canvas = FigureCanvasTkAgg(graph_fig, master=graph_frame)
canvas.draw()
canvas.get_tk_widget().pack(expand=True)


window.mainloop()