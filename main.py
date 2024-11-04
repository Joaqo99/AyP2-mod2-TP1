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

# Configuración de columnas dentro del frame 0
menus_frame.columnconfigure(0, weight=4)  # 40% ancho para el primer botón
menus_frame.columnconfigure(1, weight=3)  # 30% ancho para el segundo botón
menus_frame.columnconfigure(2, weight=3)  # 30% ancho para el tercer botón

# Frame para el gráfico (fila 1)
graph_frame = tk.Frame(window, bg="white")
graph_frame.grid(row=1, column=0, columnspan=3, sticky="nsew")


window.mainloop()

