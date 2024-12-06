import socket
import time
import tkinter as tk
from tkinter import messagebox
from vidstream import ScreenShareClient  # Asumiendo que tienes la librería de vidstream instalada

# Función para conectarse al servidor y enviar el comando
def conectar_servidor(ip, puerto_servidor, puerto_vidstream, cliente_id):
    try:
        # Crear el socket para conectarse al servidor
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((ip, puerto_servidor))

        # Enviar comando 'compartir' con un identificador para diferenciar clientes
        mensaje = f'compartir'
        client_socket.sendall(mensaje.encode('utf-8'))

        # Esperar la respuesta
        respuesta = client_socket.recv(1024).decode('utf-8')

        if respuesta == 'aceptada':
            print(f"Cliente {cliente_id} aceptado, esperando 0.5 segundos...")
            time.sleep(0.5)  # Esperar medio segundo

            # Iniciar el cliente de vidstream para este cliente, pasando el puerto de vidstream
            print(f"Iniciando cliente de vidstream para cliente {cliente_id} en el puerto {puerto_vidstream}...")
            client = ScreenShareClient(ip, puerto_vidstream)
            client.start_stream()
        else:
            print(f"Cliente {cliente_id} no aceptado por el servidor")

        # Cerrar la conexión del socket
        client_socket.close()

    except Exception as e:
        print(f"Error en cliente {cliente_id}: {e}")

# Función que maneja la interfaz gráfica y la conexión de varios clientes
def agregar_cliente():
    # Crear una nueva fila para agregar un cliente
    frame_cliente = tk.Frame(ventana, bg='blue')
    
    # Entradas para IP y puertos
    ip_entry = tk.Entry(frame_cliente)
    ip_entry.grid(row=0, column=0, padx=5, pady=5)
    ip_entry.insert(0, '127.0.0.1')  # Valor predeterminado

    puerto_servidor_entry = tk.Entry(frame_cliente)
    puerto_servidor_entry.grid(row=0, column=1, padx=5, pady=5)
    puerto_servidor_entry.insert(0, '12345')  # Valor predeterminado
    
    puerto_vidstream_entry = tk.Entry(frame_cliente)
    puerto_vidstream_entry.grid(row=0, column=2, padx=5, pady=5)
    puerto_vidstream_entry.insert(0, '8080')  # Valor predeterminado
    
    # Añadir botón para eliminar este cliente
    boton_eliminar = tk.Button(frame_cliente, text="Eliminar", command=lambda: eliminar_cliente(frame_cliente))
    boton_eliminar.grid(row=0, column=3, padx=5, pady=5)

    frame_cliente.pack(pady=5)

    # Guardar las entradas para poder acceder a ellas más tarde
    clientes.append((ip_entry, puerto_servidor_entry, puerto_vidstream_entry))

# Función para eliminar un cliente
def eliminar_cliente(frame_cliente):
    frame_cliente.destroy()
    clientes.remove(frame_cliente)

# Función que maneja la conexión de todos los clientes
def iniciar_conexion():
    # Recorrer todos los clientes y hacer la conexión
    for i, (ip_entry, puerto_servidor_entry, puerto_vidstream_entry) in enumerate(clientes):
        ip = ip_entry.get()
        puerto_servidor = int(puerto_servidor_entry.get())
        puerto_vidstream = int(puerto_vidstream_entry.get())

        if not ip or not puerto_servidor or not puerto_vidstream:
            messagebox.showerror("Error", "Por favor, ingrese todos los campos")
            return

        # Conectar a cada cliente
        conectar_servidor(ip, puerto_servidor, puerto_vidstream, i + 1)  # El índice +1 como ID del cliente

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Conexión de Múltiples Clientes a Servidor")
ventana.geometry("500x400")  # Tamaño de la ventana
ventana.configure(bg='blue')  # Fondo azul

# Lista para almacenar los clientes agregados
clientes = []

# Etiquetas
tk.Label(ventana, text="Agrega Clientes", bg='blue', fg='white').pack(pady=10)

# Botón para agregar un cliente
boton_agregar = tk.Button(ventana, text="Agregar Cliente", command=agregar_cliente, bg='green', fg='white')
boton_agregar.pack(pady=10)

# Botón para conectar todos los clientes
boton_conectar = tk.Button(ventana, text="Conectar Todos", command=iniciar_conexion, bg='green', fg='white')
boton_conectar.pack(pady=20)

# Iniciar la interfaz
ventana.mainloop()
