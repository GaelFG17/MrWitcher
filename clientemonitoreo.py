import tkinter as tk
from tkinter import messagebox
from vidstream import CameraClient, VideoClient, ScreenShareClient
import threading

# Variables globales para el cliente
client = None
streaming_thread = None

# Función para iniciar el streaming en un hilo separado
def iniciar_streaming():
    global client, streaming_thread
    ip = ip_entry.get()
    puerto = int(port_entry.get())
    opcion = opcion_var.get()

    # Configura el tipo de cliente basado en la selección
    if opcion == "Cámara":
        client = CameraClient(ip, puerto)
    elif opcion == "Video":
        video_path = video_entry.get()
        if not video_path:
            messagebox.showerror("Error", "Por favor, ingrese la ruta del video.")
            return
        client = VideoClient(ip, puerto, video_path)
    elif opcion == "Pantalla":
        client = ScreenShareClient(ip, puerto)

    # Iniciar el streaming en un hilo separado
    streaming_thread = threading.Thread(target=start_stream)
    streaming_thread.start()
    start_button.config(state="disabled")
    stop_button.config(state="normal")

# Función que realmente inicia el streaming (para el hilo separado)
def start_stream():
    try:
        client.start_stream()
        messagebox.showinfo("Éxito", f"Transmisión iniciada con {opcion_var.get()}")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo iniciar el streaming: {e}")

# Función para detener el streaming
def detener_streaming():
    global client
    if client:
        client.stop_stream()
        messagebox.showinfo("Detenido", "Transmisión detenida")
        start_button.config(state="normal")
        stop_button.config(state="disabled")

# Interfaz gráfica
root = tk.Tk()
root.title("Cliente de Streaming")
root.geometry("350x350")

# Campo de entrada para la IP
tk.Label(root, text="IP del Servidor:").pack(pady=5)
ip_entry = tk.Entry(root)
ip_entry.pack()

# Campo de entrada para el puerto
tk.Label(root, text="Puerto:").pack(pady=5)
port_entry = tk.Entry(root)
port_entry.pack()

# Campo para seleccionar el tipo de cliente
tk.Label(root, text="Seleccione el tipo de cliente:").pack(pady=10)
opcion_var = tk.StringVar(value="Cámara")
tk.Radiobutton(root, text="Cámara", variable=opcion_var, value="Cámara").pack()
tk.Radiobutton(root, text="Video", variable=opcion_var, value="Video").pack()
tk.Radiobutton(root, text="Pantalla", variable=opcion_var, value="Pantalla").pack()

# Campo para ingresar la ruta del video (solo se muestra si se selecciona "Video")
tk.Label(root, text="Ruta del Video (si aplica):").pack(pady=5)
video_entry = tk.Entry(root)
video_entry.pack()

# Botones para iniciar y detener el streaming
start_button = tk.Button(root, text="Iniciar Streaming", command=iniciar_streaming)
start_button.pack(pady=10)

stop_button = tk.Button(root, text="Detener Streaming", command=detener_streaming, state="disabled")
stop_button.pack(pady=10)

# Inicia la interfaz
root.mainloop()
