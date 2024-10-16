import socket
import threading
import tkinter as tk
from tkinter import scrolledtext

def recibir_mensajes(conn, chat_text):
    while True:
        try:
            mensaje = conn.recv(1024).decode('utf-8')
            if mensaje.lower() == "salir":
                chat_text.insert(tk.END, "El cliente ha salido del chat.\n")
                break
            chat_text.insert(tk.END, f"Cliente: {mensaje}\n")
            chat_text.see(tk.END)
        except:
            chat_text.insert(tk.END, "Conexión cerrada.\n")
            break

def enviar_mensajes(conn, entrada_mensaje, chat_text):
    mensaje = entrada_mensaje.get()
    entrada_mensaje.delete(0, tk.END)
    conn.sendall(mensaje.encode('utf-8'))
    chat_text.insert(tk.END, f"Tú: {mensaje}\n")
    chat_text.see(tk.END)
    if mensaje.lower() == "salir":
        chat_text.insert(tk.END, "Saliendo del chat...\n")
        conn.close()

def iniciar_servidor_chat():
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind(("0.0.0.0", 9090))
    servidor.listen(1)
    print("Esperando conexión de un cliente...")
    
    conn, addr = servidor.accept()
    print(f"Conexión establecida con {addr}")
    
    # Configuración de la interfaz
    ventana = tk.Tk()
    ventana.title("Servidor de Chat")

    chat_text = scrolledtext.ScrolledText(ventana, wrap=tk.WORD, width=50, height=20, state='normal')
    chat_text.pack(padx=10, pady=10)
    
    entrada_mensaje = tk.Entry(ventana, width=50)
    entrada_mensaje.pack(padx=10, pady=5)

    boton_enviar = tk.Button(ventana, text="Enviar", command=lambda: enviar_mensajes(conn, entrada_mensaje, chat_text))
    boton_enviar.pack(pady=5)

    # Crear hilo para recibir mensajes
    hilo_recibir = threading.Thread(target=recibir_mensajes, args=(conn, chat_text))
    hilo_recibir.start()

    ventana.protocol("WM_DELETE_WINDOW", lambda: conn.close() or ventana.destroy())
    ventana.mainloop()

    conn.close()
    servidor.close()

iniciar_servidor_chat()