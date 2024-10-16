import tkinter as tk
from tkinter import messagebox
import subprocess

# Función para ejecutar un archivo de Python específico
def ejecutar_archivo(archivo):
    try:
        # Ejecuta el archivo en un proceso separado
        subprocess.Popen(["python3", archivo])
        messagebox.showinfo("Éxito", f"{archivo} se está ejecutando.")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo ejecutar {archivo}: {e}")

# Interfaz gráfica
root = tk.Tk()
root.title("Menú de Ejecución de Scripts")
root.geometry("300x250")

# Título
tk.Label(root, text="Selecciona el script a ejecutar", font=("Helvetica", 14)).pack(pady=10)

# Botones para cada archivo de Python
boton1 = tk.Button(root, text="CLIENTE", command=lambda: ejecutar_archivo("clientechat.py"))
boton1.pack(pady=5)

boton2 = tk.Button(root, text="SERVIDOR", command=lambda: ejecutar_archivo("servidorchat.py"))
boton2.pack(pady=5)
root.mainloop()
