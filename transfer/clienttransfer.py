import socket
import os
import tkinter as tk
from tkinter import filedialog, messagebox

# Función para enviar el archivo
def send_file(filename, host, port):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))

        # Enviar el nombre del archivo
        client_socket.send(os.path.basename(filename).encode('utf-8'))

        # Esperar confirmación de recepción del nombre del archivo
        confirmation = client_socket.recv(1024)
        if confirmation != b"Filename received":
            messagebox.showerror("Error", "Error al enviar el nombre del archivo.")
            client_socket.close()
            return

        # Enviar el archivo en binario
        with open(filename, 'rb') as f:
            while True:
                data = f.read(1024)
                if not data:
                    break
                client_socket.send(data)

        messagebox.showinfo("Éxito", f"Archivo {filename} enviado exitosamente.")
        client_socket.close()

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo enviar el archivo: {e}")

# Función para seleccionar el archivo
def select_file():
    filename = filedialog.askopenfilename()  # Abre el cuadro de diálogo de selección de archivos
    return filename

# Función para iniciar el proceso de envío
def iniciar_envio():
    host = ip_entry.get()
    try:
        port = int(port_entry.get())
    except ValueError:
        messagebox.showerror("Error", "Por favor, ingresa un puerto válido.")
        return

    if not host or not port:
        messagebox.showwarning("Advertencia", "Por favor, ingrese la IP y el puerto.")
        return

    filename = select_file()  # Llama a la función para seleccionar el archivo
    if filename:  # Verifica que se haya seleccionado un archivo
        send_file(filename, host, port)
    else:
        messagebox.showwarning("Advertencia", "No se ha seleccionado ningún archivo.")

# Interfaz gráfica
root = tk.Tk()
root.title("Cliente de Envío de Archivos")
root.geometry("400x300")

# Campo de entrada para la IP del servidor
tk.Label(root, text="IP del Servidor:").pack(pady=5)
ip_entry = tk.Entry(root)
ip_entry.pack(pady=5)

# Campo de entrada para el puerto del servidor
tk.Label(root, text="Puerto:").pack(pady=5)
port_entry = tk.Entry(root)
port_entry.pack(pady=5)

# Botón para seleccionar el archivo y enviar
boton_enviar = tk.Button(root, text="Seleccionar Archivo y Enviar", command=iniciar_envio)
boton_enviar.pack(pady=20)

# Inicia la interfaz
root.mainloop()
