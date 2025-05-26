import tkinter as tk
import os
import random
import shutil
import time

# Ruta con archivos de prueba
RUTA_OBJETIVO = os.path.expanduser("~/ransom_prueba")
RUTA_BACKUP = os.path.expanduser("~/ransom_backup")
CLAVE_CORRECTA = "petazeta21"
TIEMPO_ESPERA = 600  # 10 minutos en segundos
PAUSA_VENTANAS = 15   # 15 segundos pausa tras intento fallido

ventanas_activas = []
bloqueo_activo = False
contador_restante = None

# Simula el cifrado renombrando archivos y sobreescribiendo su contenido
def cifrar_archivos():
    if not os.path.exists(RUTA_OBJETIVO):
        os.makedirs(RUTA_OBJETIVO)
        for i in range(5):
            with open(os.path.join(RUTA_OBJETIVO, f"documento{i}.txt"), "w") as f:
                f.write(f"Este es un archivo de prueba {i}\n")

    if not os.path.exists(RUTA_BACKUP):
        os.makedirs(RUTA_BACKUP)

    for archivo in os.listdir(RUTA_OBJETIVO):
        path = os.path.join(RUTA_OBJETIVO, archivo)
        if os.path.isfile(path) and not path.endswith(".locked"):
            with open(path, "r") as f:
                contenido = f.read()
            with open(os.path.join(RUTA_BACKUP, archivo), "w") as f:
                f.write(contenido)
            with open(path, "w") as f:
                f.write("Tus archivos han sido cifrados por Petazeta21 :)")
            os.rename(path, path + ".locked")

# Simula el descifrado restaurando los nombres de archivo y contenido original
def descifrar_archivos():
    for archivo in os.listdir(RUTA_OBJETIVO):
        path = os.path.join(RUTA_OBJETIVO, archivo)
        if path.endswith(".locked"):
            nombre_original = archivo.replace(".locked", "")
            path_backup = os.path.join(RUTA_BACKUP, nombre_original)
            if os.path.exists(path_backup):
                with open(path_backup, "r") as f:
                    contenido_original = f.read()
                with open(os.path.join(RUTA_OBJETIVO, nombre_original), "w") as f:
                    f.write(contenido_original)
            os.remove(path)
    if os.path.exists(RUTA_BACKUP):
        shutil.rmtree(RUTA_BACKUP)

# Crea una nueva ventana emergente con diseño tipo pestaña
def crear_ventana_aleatoria():
    if not bloqueo_activo:
        while True:
            x = random.randint(0, ancho - 300)
            y = random.randint(0, alto - 150)
            
            # Coordenadas de la zona central que NO debe ser tapada
            zona_x1 = ancho // 2 - 250
            zona_x2 = ancho // 2 + 250
            zona_y1 = alto // 2 - 150
            zona_y2 = alto // 2 + 150

            # Si el punto generado está dentro de esa zona prohibida, descártalo
            if not (zona_x1 < x < zona_x2 and zona_y1 < y < zona_y2):
                break

        ventana = tk.Toplevel()
        ventana.title("Petazeta21 - Advertencia")
        ventana.geometry(f"300x150+{x}+{y}")
        ventana.attributes('-topmost', False)
        ventana.overrideredirect(True)

        marco = tk.Frame(ventana, bg="#ffdddd", bd=2, relief="raised")
        marco.pack(expand=True, fill="both")
        encabezado = tk.Frame(marco, bg="#cc0000")
        encabezado.pack(fill="x")
        tk.Label(encabezado, text="¡ALERTA!", fg="white", bg="#cc0000", font=("Arial", 12, "bold")).pack(padx=5, pady=2)

        cuerpo = tk.Frame(marco, bg="#fff0f0")
        cuerpo.pack(expand=True, fill="both")
        tk.Label(cuerpo, text="Tus archivos han sido cifrados\npor Petazeta21", fg="black", bg="#fff0f0", font=("Arial", 10)).pack(pady=20)

        ventanas_activas.append(ventana)
        ventana.after(60000, lambda: cerrar_ventana(ventana))

# Cierra una ventana específica y la elimina del seguimiento
def cerrar_ventana(ventana):
    if ventana in ventanas_activas:
        ventanas_activas.remove(ventana)
    ventana.destroy()

# Interfaz gráfica con botón central
class RansomwareSimulador:
    def __init__(self, root):
        self.root = root
        root.title("Petazeta21 - Simulador de Ransomware")
        root.attributes('-fullscreen', False)
        root.attributes('-topmost', True)
        root.lift()
        root.protocol("WM_DELETE_WINDOW", self.bloquear_cierre)

        self.cuadro = tk.Frame(root, bg="white", padx=20, pady=20)
        self.cuadro.place(relx=0.5, rely=0.5, anchor="center")
        self.intentos = 0
        self.entrada_activada = True

        tk.Label(self.cuadro, text="Tus archivos han sido cifrados", fg="red", font=("Arial", 16)).pack(pady=10)
        tk.Label(self.cuadro, text="Introduce la clave para restaurarlos:").pack()

        self.entrada = tk.Entry(self.cuadro, show="*")
        self.entrada.pack(pady=5)
        self.boton = tk.Button(self.cuadro, text="Desbloquear", command=self.verificar_clave)
        self.boton.pack(pady=5)
        self.estado = tk.Label(self.cuadro, text="", fg="blue")
        self.estado.pack(pady=10)
        self.temporizador = tk.Label(self.cuadro, text="")
        self.temporizador.pack()

        self.generar_ventanas()

    def bloquear_cierre(self):
        pass  # Ignora el intento de cerrar la ventana

    def verificar_clave(self):
        global bloqueo_activo
        if not self.entrada_activada:
            return

        if self.entrada.get() == CLAVE_CORRECTA:
            self.estado.config(text="✔ Archivos restaurados correctamente.")
            descifrar_archivos()
            for v in ventanas_activas:
                v.destroy()
            self.root.destroy()
        else:
            self.intentos += 1
            self.estado.config(text="❌ Clave incorrecta. Espera 10 minutos para volver a intentarlo.")
            self.entrada_activada = False
            self.boton.config(state="disabled")
            bloqueo_activo = True
            self.temporizador_contador(TIEMPO_ESPERA)
            self.root.after(PAUSA_VENTANAS * 1000, self.reactivar_generador)
            self.root.after(TIEMPO_ESPERA * 1000, self.reactivar_entrada)

    def reactivar_entrada(self):
        global bloqueo_activo
        self.entrada_activada = True
        self.boton.config(state="normal")
        self.estado.config(text="Puedes volver a intentarlo.")
        bloqueo_activo = False
        self.temporizador.config(text="")

    def reactivar_generador(self):
        self.generar_ventanas()

    def generar_ventanas(self):
        if not bloqueo_activo:
            crear_ventana_aleatoria()
            self.root.after(3000, self.generar_ventanas)

    def temporizador_contador(self, tiempo_restante):
        if tiempo_restante > 0:
            mins, secs = divmod(tiempo_restante, 60)
            self.temporizador.config(text=f"Tiempo de espera: {mins:02d}:{secs:02d}")
            self.root.after(1000, lambda: self.temporizador_contador(tiempo_restante - 1))

if __name__ == "__main__":
    cifrar_archivos()
    root = tk.Tk()
    ancho = root.winfo_screenwidth()
    alto = root.winfo_screenheight()
    app = RansomwareSimulador(root)
    root.mainloop()
