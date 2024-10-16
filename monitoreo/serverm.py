import tkinter as tk
from vidstream import StreamingServer
import threading
from tkinter import messagebox

# Variables globales
server = None
server_thread = None

# Función para iniciar el servidor
def iniciar_servidor():
    global server, server_thread
    ip = ip_entry.get()
    puerto = int(port_entry.get())
    
    # Inicializa y ejecuta el servidor en un hilo separado
    server = StreamingServer(ip, puerto)
    server_thread = threading.Thread(target=server.start_server)
    server_thread.start()
    messagebox.showinfo("Éxito", "Servidor iniciado")
    iniciar_button.config(state="disabled")
    detener_button.config(state="normal")

# Función para detener el servidor
def detener_servidor():
    global server
    if server:
        server.stop_server()
        messagebox.showinfo("Detenido", "Servidor detenido")
        iniciar_button.config(state="normal")
        detener_button.config(state="disabled")

# Interfaz gráfica
root = tk.Tk()
root.title("Servidor de Streaming")
root.geometry("300x200")

# Campo de entrada para la IP
tk.Label(root, text="IP del Servidor:").pack(pady=5)
ip_entry = tk.Entry(root)
ip_entry.pack()

# Campo de entrada para el puerto
tk.Label(root, text="Puerto:").pack(pady=5)
port_entry = tk.Entry(root)
port_entry.pack()

# Botones para iniciar y detener el servidor
iniciar_button = tk.Button(root, text="Iniciar Servidor", command=iniciar_servidor)
iniciar_button.pack(pady=10)

detener_button = tk.Button(root, text="Detener Servidor", command=detener_servidor, state="disabled")
detener_button.pack(pady=10)

# Inicia la interfaz
root.mainloop()
