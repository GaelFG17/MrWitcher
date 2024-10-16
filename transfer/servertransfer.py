import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
from tkinter import filedialog

def start_server_gui(host='0.0.0.0', port=5001):
    def server_thread():
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((host, port))
        server_socket.listen(1)
        gui_log.insert(tk.END, f'Servidor escuchando en {host}:{port}\n')
        
        while True:
            client_socket, addr = server_socket.accept()
            gui_log.insert(tk.END, f'Conexión desde {addr}\n')
            gui_log.see(tk.END)
            
            filename_data = client_socket.recv(1024)
            try:
                filename = filename_data.decode('utf-8')
                gui_log.insert(tk.END, f'Recibiendo archivo: {filename}\n')
                gui_log.see(tk.END)
            except UnicodeDecodeError:
                gui_log.insert(tk.END, "Error al decodificar el nombre del archivo.\n")
                gui_log.see(tk.END)
                client_socket.close()
                continue

            client_socket.send(b"Filename received")

            with open(filename, 'wb') as f:
                while True:
                    data = client_socket.recv(1024)
                    if not data:
                        break
                    f.write(data)

            gui_log.insert(tk.END, f'Archivo {filename} recibido\n')
            gui_log.see(tk.END)
            client_socket.close()

    # Configuración de la interfaz gráfica
    ventana = tk.Tk()
    ventana.title("Servidor de Recepción de Archivos")
    
    # Área de texto para mostrar logs
    gui_log = scrolledtext.ScrolledText(ventana, wrap=tk.WORD, width=50, height=20)
    gui_log.pack(padx=10, pady=10)
    
    # Botón para iniciar el servidor
    start_button = tk.Button(ventana, text="Iniciar Servidor", command=lambda: threading.Thread(target=server_thread).start())
    start_button.pack(pady=5)

    ventana.mainloop()

if __name__ == '__main__':
    start_server_gui()