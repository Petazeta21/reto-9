import tkinter as tk

# Inicializar pantalla oculta
pantalla = tk.Tk()
pantalla.withdraw()
ancho_pantalla = pantalla.winfo_screenwidth()
alto_pantalla = pantalla.winfo_screenheight()

# Tamaño de las ventanas
ancho_ventana = 300
alto_ventana = 100

# Posición inicial en el centro
x_pos = ancho_pantalla // 2
y_pos = alto_pantalla // 2

# Desplazamiento por paso
desplazamiento = 30

def abrir_ventana():
    global x_pos, y_pos

    nueva = tk.Toplevel()
    nueva.title("¡Infección!")
    nueva.geometry(f"{ancho_ventana}x{alto_ventana}+{x_pos}+{y_pos}")
    tk.Label(nueva, text="¡Te han atrapado!", fg="red", font=("Arial", 14)).pack(pady=20)
    nueva.after(100, lambda: nueva.lift())

    # Avanzar en diagonal
    x_pos += desplazamiento
    y_pos += desplazamiento

    # Reiniciar en eje Y (vertical) si sale por abajo
    if y_pos + alto_ventana > alto_pantalla:
        y_pos = 0  # arriba
        x_pos += desplazamiento  # moverse una columna a la derecha

    # Reiniciar en eje X (horizontal) si sale por la derecha
    if x_pos + ancho_ventana > ancho_pantalla:
        x_pos = 0  # volver a la izquierda

def generar_infinito(root):
    abrir_ventana()
    root.after(150, lambda: generar_infinito(root))  # velocidad

# Ejecutar
root = tk.Tk()
root.withdraw()
root.after(0, lambda: generar_infinito(root))
root.mainloop()
