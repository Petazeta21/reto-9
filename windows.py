import tkinter as tk

# Variables globales para las coordenadas
x_pos = 100
y_pos = 100
desplazamiento = 20  # distancia entre cada ventana

def abrir_ventana():
    global x_pos, y_pos

    nueva = tk.Toplevel()
    nueva.title("¡Infección!")
    nueva.geometry(f"300x100+{x_pos}+{y_pos}")  # Posición específica

    tk.Label(nueva, text="¡Te han atrapado!", fg="red", font=("Arial", 14)).pack(pady=20)
    nueva.after(100, lambda: nueva.lift())

    # Actualizar coordenadas para la siguiente ventana
    x_pos += desplazamiento
    y_pos += desplazamiento

    # Opcional: reiniciar si llegan al borde de pantalla
    if x_pos > 1000 or y_pos > 700:
        x_pos, y_pos = 100, 100

def generar_infinito(root):
    abrir_ventana()
    root.after(300, lambda: generar_infinito(root))

# Ventana principal (oculta)
root = tk.Tk()
root.withdraw()
root.after(0, lambda: generar_infinito(root))
root.mainloop()

