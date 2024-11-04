import tkinter as tk

#ventana principal
window = tk.Tk()
window.title("Transmission Loss Calculator")
window.geometry("1000x600")
window.configure(bg="gray")


#Segmentación de contenedores
window.rowconfigure(0, weight=2) #menus
window.rowconfigure(1, weight=8) # gráficos

# Columnas de menus
window.columnconfigure(0, weight=4)  # Opciones
window.columnconfigure(1, weight=3)  # Funciones
window.columnconfigure(2, weight=3)  # Métodos de cálculo

# Frame de Menus
menus_frame = tk.Frame(window, bg="lightgray")
menus_frame.grid(row=0, column=0, columnspan=3, sticky="nsew")

menus_frame.columnconfigure(0, weight=4)  
menus_frame.columnconfigure(1, weight=3)
menus_frame.columnconfigure(2, weight=3)  

menus_frame.grid_propagate(False)

#menú opciones
options_frame = tk.LabelFrame(menus_frame, text="Opciones", bg="lightgray")
options_frame.grid(row=0, column=0, sticky="nsew")

materiales_label = tk.Label(options_frame, text="Materiales", bg="lightgray")
materiales_label.pack()


#menú funciones
functions_frame = tk.LabelFrame(menus_frame, text="Funciones", bg="lightgray")
functions_frame.grid(row=0, column=1, sticky="nsew")

boton_procesar = tk.Button(functions_frame, text="Procesar")
boton_exportar = tk.Button(functions_frame, text="Exportar")
boton_borrar = tk.Button(functions_frame, text="Borrar")

boton_procesar.pack(), boton_exportar.pack(), boton_borrar.pack()

# Frame para el gráfico (fila 1)
graph_frame = tk.Frame(window, bg="white")
graph_frame.grid(row=1, column=0, columnspan=3, sticky="nsew")


window.mainloop()

