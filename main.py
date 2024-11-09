import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import materiales

# Ventana principal
window = ttk.Window(themename="superhero")
window.title("Transmission Loss Calculator")
window.geometry("1300x700")

# Segmentación de contenedores
window.rowconfigure(0, weight=1)  # Menús
window.rowconfigure(1, weight=20) # Gráficos

# Columnas de menús
window.columnconfigure(0, minsize=600, weight=2)  
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

largo_label = ttk.Label(frame_inferior, text="Largo:")
largo_label.grid(row=0, column=1, padx=5, pady=5, sticky="e")
largo_entry = ttk.Entry(frame_inferior, width=5)
largo_entry.grid(row=0, column=2, padx=5, pady=5, sticky="w")

alto_label = ttk.Label(frame_inferior, text="Alto:")
alto_label.grid(row=0, column=3, padx=5, pady=5, sticky="e")
alto_entry = ttk.Entry(frame_inferior, width=5)
alto_entry.grid(row=0, column=4, padx=5, pady=5, sticky="w")

espesor_label = ttk.Label(frame_inferior, text="Espesor:")
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

# Botones con ttkbootstrap
boton_procesar = ttk.Button(functions_frame, text="Procesar", bootstyle=PRIMARY, padding=3, width=14)
boton_agregar_material = ttk.Button(functions_frame, text="Agregar Material", bootstyle=SECONDARY, padding=3, width=14)
boton_exportar = ttk.Button(functions_frame, text="Exportar", bootstyle=SECONDARY, padding=3, width=14)
boton_borrar = ttk.Button(functions_frame, text="Borrar", bootstyle=DANGER, padding=3, width=14)

boton_procesar.grid(row=0, column=0, padx=5, pady=5)
boton_agregar_material.grid(row=0, column=1, padx=5, pady=5)
boton_exportar.grid(row=1, column=0, padx=5, pady=5)
boton_borrar.grid(row=1, column=1, padx=5, pady=5)

###########################
# Menú de métodos de cálculo
davy = ttk.BooleanVar()
pared_simple = ttk.BooleanVar()
sharp = ttk.BooleanVar()
iso = ttk.BooleanVar()

methods_frame = ttk.Labelframe(window, text="Métodos de cálculo")
methods_frame.grid(row=0, column=2, sticky="nsew", padx=10, pady=5)

methods_frame.columnconfigure(0, weight=1)
methods_frame.columnconfigure(1, weight=1)
methods_frame.rowconfigure(0, weight=1)
methods_frame.rowconfigure(1, weight=1)

davy_check = ttk.Checkbutton(methods_frame, text="Davy", variable=davy)
pared_simple_check = ttk.Checkbutton(methods_frame, text="Pared Simple", variable=pared_simple)
sharp_check = ttk.Checkbutton(methods_frame, text="Sharp", variable=sharp)
iso_check = ttk.Checkbutton(methods_frame, text="ISO", variable=iso)

davy_check.grid(row=0, column=0, sticky="w", padx=5, pady=5)
pared_simple_check.grid(row=0, column=1, sticky="w", padx=5, pady=5)
sharp_check.grid(row=1, column=0, sticky="w", padx=5, pady=5)
iso_check.grid(row=1, column=1, sticky="w", padx=5, pady=5)

# Frame para el gráfico
graph_frame = ttk.Frame(window, bootstyle="secondary")
graph_frame.grid(row=1, column=0, columnspan=3, sticky="nsew", padx=10, pady=5)

window.mainloop()