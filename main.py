import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
import materiales
import plot
import export
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

from acoustics_functions_Sharp import sharp_method
from acoustics_functions_Davy_main import davy_method
from acoustics_function_Cremer import cremer_method
from acoustics_functions_ISO12354_main import iso_method


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

def reset_entry_styles():
    largo_entry.configure(bootstyle="default")
    alto_entry.configure(bootstyle="default")
    espesor_entry.configure(bootstyle="default")


def show_error_message(message):
    # Crear la ventana de error
    error_win = ttk.Toplevel(window)
    error_win.title("Error")
    error_win.geometry("300x150")  # Tamaño de la ventana de error

    # Centrar la ventana en la pantalla
    error_win.update_idletasks()  # Asegurarse de que las dimensiones están actualizadas
    screen_width = error_win.winfo_screenwidth()
    screen_height = error_win.winfo_screenheight()
    x = (screen_width - error_win.winfo_width()) // 2
    y = (screen_height - error_win.winfo_height()) // 2
    error_win.geometry(f"+{x}+{y}")

    # Configuración de contenido en la ventana de error
    error_label = ttk.Label(error_win, text=message, wraplength=250, bootstyle="danger")
    error_label.pack(pady=20)

    ok_button = ttk.Button(error_win, text="Aceptar", command=error_win.destroy)
    ok_button.pack(pady=10)

    # Hacer que la ventana sea modal para evitar interacciones con la ventana principal
    error_win.transient(window)  # Indicar que es hija de la ventana principal
    error_win.grab_set()
    window.wait_window(error_win)  # Esperar hasta que la ventana de error se cierre


def validate_inputs():
    reset_entry_styles()
    valid = True
    # Verificar si se ha seleccionado un material
    if selected_material.get() == "Material":
        show_error_message("Seleccione un material.")
        valid = False
    
    # Verificar si las dimensiones son válidas
    try:
        largo = float(largo_entry.get())
        alto = float(alto_entry.get())
        espesor = float(espesor_entry.get())
        if largo <= 0 or alto <= 0 or espesor <= 0:
            raise ValueError
    except ValueError:
        show_error_message("Ingrese dimensiones válidas.")
        largo_entry.configure(bootstyle="danger")  # Resaltar campo en rojo
        alto_entry.configure(bootstyle="danger")
        espesor_entry.configure(bootstyle="danger")
        valid = False
    
    # Verificar si al menos un método de cálculo está seleccionado
    if not (davy.get() or sharp.get() or iso.get() or cremer.get()):
        show_error_message("Seleccione al menos un método de cálculo.")
        valid = False

    return valid



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
    materiales_menu.add_radiobutton(label=mat, variable=selected_material, value=mat)



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

    if not validate_inputs():
        return

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

    if iso.get():
        f_c, R_values["R_iso"] = iso_method(material, largo, alto,  espesor)
    else:
        R_values["R_iso"] = None

    if cremer.get():
        f_c, R_values["R_cremer"] = cremer_method(material, espesor)
    else:
        R_values["R_cremer"] = None

    # Actualizar los datos de las líneas sin recrear el gráfico
    plot.update_plot(lines, R_values, f_c)  # Pasamos las líneas y los nuevos valores de R
    canvas.draw()

    #hacer control de errores si no hay nada seleccionado


boton_procesar = ttk.Button(functions_frame, text="Procesar", bootstyle=PRIMARY, padding=3, width=14, command=procesar)
boton_procesar.grid(row=0, column=0, padx=5, pady=5)


#agregar material
def nuevo_material():

    def agregar_material():
        try:
            # Obtener y validar los valores ingresados
            nombre = nombre_entry.get()
            densidad = float(den_entry.get())
            ym = float(ym_entry.get())
            lf = float(lf_entry.get())
            pm = float(pm_entry.get())
            
            if not nombre:
                raise ValueError("Ingrese un nombre válido.")
            
            # Si la validación es exitosa, se crea el diccionario y se añade el material
            new_mat_dict = {
                "Name": nombre,
                "Den": densidad,
                "YM": ym,
                "LF": lf,
                "PM": pm,
            }
            
            materiales.add_material(new_mat_dict)
            materiales_menu.add_radiobutton(label=nombre, variable=selected_material, value=nombre)
            
            # Cerrar la ventana solo si todo es válido
            add_mat_win.destroy()
            
        except ValueError:
            # Mostrar mensaje de error si hay valores inválidos
            show_error_message("Datos faltantes o inválidos para el material.")

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
def exportar():

    if not any(R_values.values()):
        show_error_message("Realice un cálculo antes de exportar.")
        return

    material = selected_material.get()
    largo = float(largo_entry.get())
    alto = float(alto_entry.get())
    espesor = float(espesor_entry.get())

    export.exportar_datos(material, largo, alto, espesor, R_values, f_c)

    mb = Messagebox.yesno("Datos exportados. ∖nDesea realizar informe?")

boton_exportar = ttk.Button(functions_frame, text="Exportar", bootstyle=SECONDARY, padding=3, width=14, command=exportar)
boton_exportar.grid(row=1, column=0, padx=5, pady=5)

#borrar

def borrar():
    # Llamar a la función clear_plot para borrar las líneas del gráfico
    plot.clear_plot(lines)
    
    # Limpiar las entradas 
    largo_entry.delete(0, "end")
    alto_entry.delete(0, "end")
    espesor_entry.delete(0, "end")
    selected_material.set("Material")

    davy.set(0)
    iso.set(0)
    cremer.set(0)
    sharp.set(0)

    R_values["R_sharp"] = None
    R_values["R_davy"] = None
    R_values["R_iso"] = None
    R_values["R_cremer"] = None

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
iso_check = ttk.Checkbutton(methods_frame, text="ISO 12354-1", variable=iso)

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