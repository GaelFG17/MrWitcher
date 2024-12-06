import socket
import tkinter as tk
from tkinter import messagebox

# Función para enviar comando al servidor
def enviar_comando(ip_servidor, puerto, comando):
    try:
        # Crear un socket para conectarse al servidor
        cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cliente_socket.connect((ip_servidor, puerto))  # Conectar al servidor en la IP y puerto especificados

        # Enviar el comando (bloquear/desbloquear) al servidor
        cliente_socket.send(comando.encode('utf-8'))
        print(f"[INFO] Comando '{comando}' enviado al servidor.")
        
        # Cerrar la conexión
        cliente_socket.close()

        # Mostrar mensaje de éxito
        messagebox.showinfo("Resultado", f"Comando '{comando}' enviado al servidor.")
    except Exception as e:
        print(f"[ERROR] No se pudo enviar el comando: {e}")
        messagebox.showerror("Error", f"No se pudo enviar el comando: {e}")

# Función que ejecuta el comando según la opción seleccionada
def ejecutar_comando():
    ip_servidor = entry_ip.get()  # Obtener IP desde la interfaz
    puerto = int(entry_puerto.get())  # Obtener puerto desde la interfaz
    comando = entry_comando.get()  # Obtener comando desde la interfaz

    if comando in ["bloquear", "desbloquear"]:
        enviar_comando(ip_servidor, puerto, comando)  # Enviar el comando
    else:
        messagebox.showerror("Error", "Comando no válido. Usa 'bloquear' o 'desbloquear'.")

# Interfaz gráfica
root = tk.Tk()
root.title("Enviar Comando al Servidor")
root.configure(bg="#0f2557")

# Función para el hover en los botones
def on_enter(e):
    e.widget['bg'] = "#465eff"

def on_leave(e):
    e.widget['bg'] = "#2f4b8f"

# Crear un botón con estilo personalizado
def crear_boton(texto, comando, columna, fila):
    boton = tk.Button(
        root, 
        text=texto, 
        command=comando, 
        font=("Helvetica", 10, "bold"), 
        bg="#2f4b8f", 
        fg="white", 
        width=20,  # Ancho mayor para que todos los botones tengan el mismo tamaño
        height=2,  # Altura mayor para más consistencia
        relief=tk.FLAT, 
        border=0
    )
    boton.bind("<Enter>", on_enter)
    boton.bind("<Leave>", on_leave)
    boton.grid(row=fila, column=columna, padx=5, pady=5, sticky="ew")  # Alineación horizontal (expandir) con sticky="ew"
    return boton

# Etiquetas y campos de entrada
tk.Label(root, text="IP del Servidor:", bg="#0f2557", fg="white", font=("Helvetica", 10)).grid(row=0, column=0, padx=10, pady=5)
entry_ip = tk.Entry(root, font=("Helvetica", 10))
entry_ip.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Puerto:", bg="#0f2557", fg="white", font=("Helvetica", 10)).grid(row=1, column=0, padx=10, pady=5)
entry_puerto = tk.Entry(root, font=("Helvetica", 10))
entry_puerto.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Comando (bloquear/desbloquear):", bg="#0f2557", fg="white", font=("Helvetica", 10)).grid(row=2, column=0, padx=10, pady=5)
entry_comando = tk.Entry(root, font=("Helvetica", 10))
entry_comando.grid(row=2, column=1, padx=10, pady=5)

# Botón para ejecutar el comando
crear_boton("Enviar Comando", ejecutar_comando, 0, 3)

# Ejecutar la interfaz gráfica
root.mainloop()
