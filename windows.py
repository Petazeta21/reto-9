import tkinter as tk

# Función que crea una nueva ventana
def abrir_ventana():
    nueva = tk.Toplevel()
    nueva.title("¡Infección!")
    nueva.geometry("300x100")
    tk.Label(nueva, text="¡Te han atrapado!", fg="red", font=("Arial", 14)).pack(pady=20)
    nueva.after(100, lambda: nueva.lift())  # Mantener al frente

# Función recursiva que genera ventanas sin parar
def generar_infinito(root):
    abrir_ventana()
    root.after(300, lambda: generar_infinito(root))  # cada 300 ms

# Ventana principal oculta
root = tk.Tk()
root.withdraw()  # No mostrar ventana base

# Iniciar el bucle de infección visual
root.after(0, lambda: generar_infinito(root))
root.mainloop()

