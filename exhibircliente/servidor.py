import socket
import tkinter as tk
from tkinter import messagebox

# Conexión al socket de Cliente 1
def conectar_a_cliente1(ip_cliente1, puerto_cliente1):
    try:
        # Conexión al socket de Cliente 1
        cliente1_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cliente1_socket.connect((ip_cliente1, int(puerto_cliente1)))
        print("[INFO] Conexión exitosa con Cliente 1.")

        # Enviar el comando 'exhibir' a Cliente 1
        cliente1_socket.sendall("exhibir".encode('utf-8'))
        print("[INFO] Comando 'exhibir' enviado a Cliente 1.")
        
        cliente1_socket.close()
    except Exception as e:
        print(f"[ERROR] No se pudo conectar a Cliente 1: {e}")
        messagebox.showerror("Error", f"No se pudo conectar a Cliente 1: {e}")

# Conexión a Cliente 2
def conectar_a_cliente2(ip_cliente2, puerto_cliente2, ip_cliente1, puerto_cliente1):
    try:
        # Conexión a Cliente 2
        cliente2_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cliente2_socket.connect((ip_cliente2, int(puerto_cliente2)))
        print("[INFO] Conexión exitosa con Cliente 2.")
        
        # Enviar el comando 'compartir' a Cliente 2
        cliente2_socket.sendall("compartir".encode('utf-8'))
        print("[INFO] Comando 'compartir' enviado a Cliente 2.")

        # Esperar la respuesta de Cliente 2 (aceptada o rechazada)
        respuesta = cliente2_socket.recv(1024).decode('utf-8')
        if respuesta == "aceptada":
            print("[INFO] Cliente 2 aceptó compartir pantalla.")
            # Ahora que Cliente 2 aceptó, se envía el comando a Cliente 1
            conectar_a_cliente1(ip_cliente1, puerto_cliente1)
        else:
            print("[INFO] Cliente 2 rechazó compartir pantalla.")
        
        cliente2_socket.close()
    except Exception as e:
        print(f"[ERROR] No se pudo conectar a Cliente 2: {e}")
        messagebox.showerror("Error", f"No se pudo conectar a Cliente 2: {e}")

# Función principal para iniciar la comunicación entre los clientes
def iniciar_comunicacion():
    ip_cliente1 = entry_ip_cliente1.get()
    puerto_cliente1 = entry_puerto_cliente1.get()
    ip_cliente2 = entry_ip_cliente2.get()
    puerto_cliente2 = entry_puerto_cliente2.get()
    
    if not ip_cliente1 or not puerto_cliente1 or not ip_cliente2 or not puerto_cliente2:
        messagebox.showwarning("Advertencia", "Por favor ingresa todas las IPs y puertos.")
        return

    # Conectar a Cliente 2 y enviar el comando 'compartir'
    conectar_a_cliente2(ip_cliente2, puerto_cliente2, ip_cliente1, puerto_cliente1)

# Función para manejar el efecto hover en los botones
def on_enter(e):
    e.widget['background'] = '#6a5acd'  # Color de hover morado

def on_leave(e):
    e.widget['background'] = '#ffffff'  # Color normal blanco

# Crear la ventana de la interfaz gráfica
ventana = tk.Tk()
ventana.title("Conexión de Clientes")
ventana.geometry("400x400")
ventana.config(bg="#0f2557")  # Fondo morado

# Etiqueta en la interfaz para indicar la acción
etiqueta = tk.Label(ventana, text="Iniciar comunicación", fg="white", bg="#0f2557", font=("Arial", 16))
etiqueta.pack(pady=10)

# Etiquetas y campos de texto para las IPs y puertos
label_ip_cliente1 = tk.Label(ventana, text="IP Cliente 1:", fg="white", bg="#0f2557", font=("Arial", 12))
label_ip_cliente1.pack(pady=5)
entry_ip_cliente1 = tk.Entry(ventana, font=("Arial", 12), bd=2, relief="solid")
entry_ip_cliente1.pack(pady=5)

label_puerto_cliente1 = tk.Label(ventana, text="Puerto Cliente 1:", fg="white", bg="#0f2557", font=("Arial", 12))
label_puerto_cliente1.pack(pady=5)
entry_puerto_cliente1 = tk.Entry(ventana, font=("Arial", 12), bd=2, relief="solid")
entry_puerto_cliente1.pack(pady=5)

label_ip_cliente2 = tk.Label(ventana, text="IP Cliente 2:", fg="white", bg="#0f2557", font=("Arial", 12))
label_ip_cliente2.pack(pady=5)
entry_ip_cliente2 = tk.Entry(ventana, font=("Arial", 12), bd=2, relief="solid")
entry_ip_cliente2.pack(pady=5)

label_puerto_cliente2 = tk.Label(ventana, text="Puerto Cliente 2:", fg="white", bg="#0f2557", font=("Arial", 12))
label_puerto_cliente2.pack(pady=5)
entry_puerto_cliente2 = tk.Entry(ventana, font=("Arial", 12), bd=2, relief="solid")
entry_puerto_cliente2.pack(pady=5)

# Botón para iniciar la comunicación con diseño
boton_iniciar = tk.Button(ventana, text="Iniciar", command=iniciar_comunicacion, bg="#ffffff", font=("Arial", 12), bd=2, relief="solid", padx=20, pady=10)
boton_iniciar.pack(pady=20)

# Agregar efectos hover a los botones
boton_iniciar.bind("<Enter>", on_enter)
boton_iniciar.bind("<Leave>", on_leave)

# Ejecutar la interfaz gráfica
ventana.mainloop()
