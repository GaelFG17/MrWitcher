import winrm
import tkinter as tk
from tkinter import messagebox

def apagar_pc():
    # Obtiene y divide los datos de la interfaz
    entradas = ip_credenciales_entry.get().split(";")  # Separa cada conjunto por punto y coma
    
    for entrada in entradas:
        try:
            # Separa IP, usuario y contraseña por comas
            ip, usuario, contraseña = entrada.split(",")
            ip = ip.strip()
            usuario = usuario.strip()
            contraseña = contraseña.strip()
            
            # Configura la sesión WinRM para cada IP
            session = winrm.Session(f'http://{ip}:5985/wsman', auth=(usuario, contraseña))
            
            # Ejecuta el comando de apagado
            result = session.run_cmd('shutdown', ['/s', '/f', '/t', '0'])
            
            # Muestra el resultado en la interfaz
            if result.status_code == 0:
                messagebox.showinfo("Éxito", f"La PC con IP {ip} se está apagando.")
            else:
                messagebox.showerror("Error", f"No se pudo apagar la PC con IP {ip}. Código de error: {result.status_code}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo apagar la PC con IP {ip}: {e}")

# Configuración de la interfaz gráfica
root = tk.Tk()
root.title("Apagar PCs Remotas")
root.geometry("400x350")

# Etiquetas y campos de entrada
tk.Label(root, text="IPs y Credenciales (formato: IP,usuario,contraseña; ... ):").pack(pady=5)
ip_credenciales_entry = tk.Entry(root, width=50)
ip_credenciales_entry.pack()

# Botón para ejecutar el comando de apagado
apagar_btn = tk.Button(root, text="Apagar PCs", command=apagar_pc)
apagar_btn.pack(pady=20)

# Inicia la interfaz
root.mainloop()
