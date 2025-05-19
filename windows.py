import tkinter as tk
import threading
import time

def abrir_ventana():
    while True:
        ventana = tk.Tk()
        ventana.title("¡Alerta!")
        ventana.geometry("300x100")
        etiqueta = tk.Label(ventana, text="¡Estás infectado!", fg="red", font=("Arial", 14))
        etiqueta.pack(pady=20)
        ventana.after(100, lambda: ventana.lift())  # Mantiene al frente
        threading.Thread(target=ventana.mainloop).start()
        time.sleep(0.1)  # Controla la velocidad de aparición

abrir_ventana()
