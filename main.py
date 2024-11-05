from tkinter import ttk
import tkinter as tk

#ventana principal
window = tk.Tk()
window.title("Transmission Loss Calculator")
window.geometry("1000x600")
window.configure(bg="gray")


#Segmentación de contenedores
window.rowconfigure(0, weight=1) #menus
window.rowconfigure(1, weight=20) # gráficos

# Columnas de menus
window.columnconfigure(0, weight=5)  
window.columnconfigure(1, weight=2)  
window.columnconfigure(2, weight=1)  

####################
#menú opciones
options_frame = tk.LabelFrame(window, text="Opciones", bg="lightgray")
options_frame.grid(row=0, column=0, sticky="nsew")

materiales_label = tk.Label(options_frame, text="Material", bg="lightgray")
materiales_label.pack(side="left")

materiales_menu = ttk.Combobox(options_frame)
materiales_menu.pack(side="left")

######################
#menú funciones
functions_frame = tk.LabelFrame(window, text="Funciones", bg="lightgray")
functions_frame.grid(row=0, column=1, sticky="nsew")


functions_frame.columnconfigure(0,weight=1)
functions_frame.columnconfigure(1,weight=1)
functions_frame.rowconfigure(0,weight=1)
functions_frame.rowconfigure(1,weight=1)

boton_procesar = tk.Button(functions_frame,  text="Procesar")
boton_exportar = tk.Button(functions_frame, text="Exportar")
boton_borrar = tk.Button(functions_frame, text="Borrar")

boton_procesar.config(fg="black")
boton_exportar.config(fg="black")
boton_borrar.config(fg="red")

boton_procesar.grid(row=0, column=0)
boton_exportar.grid(row=1, column=0)
boton_borrar.grid(row=1, column=1)


###########################
#Menú de métodos de cálculo

davy = tk.BooleanVar()
pared_simple = tk.BooleanVar()
sharp = tk.BooleanVar()
iso = tk.BooleanVar()

def on_check_button_cambio():
    pass

methods_frame = tk.LabelFrame(window, text="Métodos de cálculo", bg="lightgray")
methods_frame.grid(row=0, column=2, sticky="nsew")

methods_frame.columnconfigure(0,weight=1)
methods_frame.columnconfigure(1,weight=1)
methods_frame.rowconfigure(0,weight=1)
methods_frame.rowconfigure(1,weight=1)


davy_check = tk.Checkbutton(methods_frame, text="Davy", variable=davy, bg="lightgray")
pared_simple_check = tk.Checkbutton(methods_frame, text="Pared Simple", variable=pared_simple, bg="lightgray")
sharp_check = tk.Checkbutton(methods_frame, text="Sharp", variable=sharp, bg="lightgray")
iso_check = tk.Checkbutton(methods_frame, text="ISO", variable=iso, bg="lightgray")

davy_check.grid(row=0, column=0, sticky="w")
pared_simple_check.grid(row=0, column=1, sticky="w")
sharp_check.grid(row=1, column=0, sticky="w")
iso_check.grid(row=1, column=1, sticky="w")

# Frame para el gráfico (fila 1)
graph_frame = tk.Frame(window, bg="white")
graph_frame.grid(row=1, column=0, columnspan=3, sticky="nsew")

window.mainloop()

