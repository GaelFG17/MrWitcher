import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox

# Variables globales
cliente = None
conectado = False

# Función para recibir mensajes del servidor
def recibir_mensajes():
    global cliente
    while conectado:
        try:
            mensaje = cliente.recv(1024).decode('utf-8')
            if mensaje.lower() == "salir":
                chat_text.config(state=tk.NORMAL)
                chat_text.insert(tk.END, "El servidor ha salido del chat.\n")
                chat_text.config(state=tk.DISABLED)
                break
            chat_text.config(state=tk.NORMAL)
            chat_text.insert(tk.END, f"Servidor: {mensaje}\n")
            chat_text.config(state=tk.DISABLED)
            chat_text.yview(tk.END)
        except:
            chat_text.config(state=tk.NORMAL)
            chat_text.insert(tk.END, "Conexión cerrada.\n")
            chat_text.config(state=tk.DISABLED)
            break

# Función para enviar mensajes al servidor
def enviar_mensaje():
    global cliente
    mensaje = mensaje_entry.get()
    if mensaje and conectado:
        chat_text.config(state=tk.NORMAL)
        chat_text.insert(tk.END, f"Tú: {mensaje}\n")
        chat_text.config(state=tk.DISABLED)
        cliente.sendall(mensaje.encode('utf-8'))
        mensaje_entry.delete(0, tk.END)
        if mensaje.lower() == "salir":
            chat_text.config(state=tk.NORMAL)
            chat_text.insert(tk.END, "Saliendo del chat...\n")
            chat_text.config(state=tk.DISABLED)
            cliente.close()

# Función para conectar con el servidor e iniciar el chat
def conectar():
    global cliente, conectado
    host = host_entry.get()
    port = port_entry.get()
    
    if not host or not port:
        messagebox.showwarning("Advertencia", "Por favor, introduce la IP y el puerto.")
        return

    try:
        port = int(port)  # Asegura que el puerto sea un número
        cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cliente.connect((host, port))
        conectado = True
        messagebox.showinfo("Conexión", "Conectado al servidor")

        # Crear hilo para recibir mensajes
        recibir_thread = threading.Thread(target=recibir_mensajes)
        recibir_thread.start()

        # Abrir la ventana del chat
        abrir_ventana_chat()

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo conectar al servidor: {e}")

# Función para abrir la ventana del chat
def abrir_ventana_chat():
    global root, ventana_chat, mensaje_entry, chat_text, boton_enviar

    # Cierra la ventana de conexión
    root.destroy()

    # Nueva ventana para el chat
    ventana_chat = tk.Tk()
    ventana_chat.title("Chat en vivo")
    ventana_chat.geometry("400x500")

    # Cuadro de texto para mostrar los mensajes del chat
    chat_text = scrolledtext.ScrolledText(ventana_chat, wrap=tk.WORD, state=tk.DISABLED)
    chat_text.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

    # Campo de entrada para escribir el mensaje
    mensaje_entry = tk.Entry(ventana_chat, state=tk.NORMAL)
    mensaje_entry.pack(pady=5, padx=10, fill=tk.X)

    # Botón para enviar mensajes
    boton_enviar = tk.Button(ventana_chat, text="Enviar", command=enviar_mensaje)
    boton_enviar.pack(pady=10)

    # Inicia la ventana del chat
    ventana_chat.mainloop()

# Interfaz gráfica para la ventana de conexión
root = tk.Tk()
root.title("Cliente de Chat")
root.geometry("400x300")

# Campo de entrada para la IP del servidor
tk.Label(root, text="IP del Servidor:").pack(pady=5)
host_entry = tk.Entry(root)
host_entry.pack(pady=5)

# Campo de entrada para el puerto del servidor
tk.Label(root, text="Puerto:").pack(pady=5)
port_entry = tk.Entry(root)
port_entry.pack(pady=5)

# Botón para conectar
boton_conectar = tk.Button(root, text="Conectar", command=conectar)
boton_conectar.pack(pady=10)

# Inicia la interfaz de conexión
root.mainloop()
