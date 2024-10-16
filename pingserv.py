import tkinter as tk
from tkinter import simpledialog, messagebox
from ping3 import verbose_ping
import subprocess
import sys
from io import StringIO
def solicitar_contraseña():
    return simpledialog.askstring("Contraseña de administrador", "Ingresa tu contraseña de administrador:", show="*")

def ejecutar_comando_sudo(comando, password):
    comando_con_sudo = f"echo {password} | sudo -S {comando}"
    resultado = subprocess.run(comando_con_sudo, shell=True, text=True, capture_output=True)
    
    # Mostrar el resultado o error en caso de fallo
    if resultado.returncode != 0:
        print(f"Error: {resultado.stderr}")
        return False
    else:
        print(f"Éxito: {resultado.stdout}")
        return True

def pingre(ip):
    resultado_text.delete(1.0, tk.END)
    try:
        # Redirigir la salida estándar para capturar la salida de verbose_ping
        captured_output = StringIO()
        sys.stdout = captured_output

        resultado_text.insert(tk.END, f"Haciendo ping a {ip}...\n")
        verbose_ping(ip)  # Esto imprimirá el resultado en captured_output

        # Restaurar la salida estándar
        sys.stdout = sys.__stdout__

        # Insertar lo que capturamos en la interfaz gráfica
        resultado_text.insert(tk.END, captured_output.getvalue())
    except Exception as e:
        resultado_text.insert(tk.END, f"Error: {e}\n")


def ejecutar_comando_sudo(comando, password):
    comando_con_sudo = f"echo {password} | sudo -S {comando}"
    resultado = subprocess.run(comando_con_sudo, shell=True, text=True, capture_output=True)
    
    # Verificamos si hay un mensaje de advertencia relacionado con ALTQ
    if "No ALTQ support in kernel" in resultado.stderr or "ALTQ related functions disabled" in resultado.stderr:
        print("Advertencia de ALTQ ignorada.")
        return True  # Lo tratamos como éxito, ya que el comando se ejecutó correctamente

    # Mostrar el resultado o error en caso de fallo
    if resultado.returncode != 0:
        print(f"Error: {resultado.stderr}")
        return False
    else:
        print(f"Éxito: {resultado.stdout}")
        return True

def bloquear_ping_desde_ip(ip):
    regla = f"block drop in quick on en0 proto icmp from {ip} to any\n"
    password = solicitar_contraseña()
    if password is None:
        messagebox.showwarning("Advertencia", "Se requiere una contraseña para ejecutar esta acción.")
        return
    
    try:
        # Usamos sudo directamente con redirección a un archivo
        comando1 = f"echo '{regla}' | sudo tee /etc/pf.anchors/block_ping > /dev/null"
        if not ejecutar_comando_sudo(comando1, password):
            raise Exception("Error al escribir la regla de bloqueo en /etc/pf.anchors/block_ping")

        # Configurar pf.conf para cargar la regla temporal
        config = "anchor \"block_ping\"\nload anchor \"block_ping\" from \"/etc/pf.anchors/block_ping\"\n"
        comando2 = f"echo '{config}' | sudo tee -a /etc/pf.conf > /dev/null"
        if not ejecutar_comando_sudo(comando2, password):
            raise Exception("Error al actualizar /etc/pf.conf")

        # Recargar la configuración y habilitar el firewall
        resultado = subprocess.run("sudo pfctl -f /etc/pf.conf", shell=True, capture_output=True, text=True)
        # Ignorar la salida de error relacionada con ALTQ
        if resultado.returncode != 0 and "ALTQ" not in resultado.stderr:
            raise Exception("Error al recargar la configuración de pfctl")
        
        if not ejecutar_comando_sudo("sudo pfctl -e", password):
            raise Exception("Error al habilitar pfctl")
        
        # Verificación de que la regla fue añadida al archivo de configuración
        with open("/etc/pf.anchors/block_ping", "r") as file:
            reglas = file.read()
            if ip in reglas:
                messagebox.showinfo("Acción completada", f"Ping bloqueado desde {ip}.")
            else:
                messagebox.showwarning("Advertencia", f"No se pudo confirmar el bloqueo de la IP: {ip}.")
    
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo bloquear el ping: {e}")


def permitir_ping_desde_ip(ip):
    password = solicitar_contraseña()
    if password is None:
        messagebox.showwarning("Advertencia", "Se requiere una contraseña para ejecutar esta acción.")
        return
    
    try:
        # Eliminar la regla de bloqueo de /etc/pf.anchors/block_ping
        comando1 = f"sudo sed -i '' '/{ip}/d' /etc/pf.anchors/block_ping"
        if not ejecutar_comando_sudo(comando1, password):
            raise Exception("Error al eliminar la regla de bloqueo en /etc/pf.anchors/block_ping")
        
        # Eliminar la referencia a la regla de bloqueo en /etc/pf.conf
        comando2 = f"sudo sed -i '' '/block_ping/d' /etc/pf.conf"
        if not ejecutar_comando_sudo(comando2, password):
            raise Exception("Error al eliminar la referencia en /etc/pf.conf")
        
        # Recargar la configuración del firewall
        if not ejecutar_comando_sudo("sudo pfctl -f /etc/pf.conf", password):
            raise Exception("Error al recargar la configuración de pfctl")
        
        # Verificación adicional si la IP está permitida
        resultado_verificacion = subprocess.run(f"sudo pfctl -sr | grep {ip}", shell=True, capture_output=True, text=True)
        if resultado_verificacion.returncode != 0:
            messagebox.showinfo("Acción completada", f"Ping permitido desde {ip}.")
        else:
            messagebox.showwarning("Advertencia", "No se pudo verificar la eliminación del bloqueo para la IP.")
    
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo permitir el ping: {e}")


def realizar_accion(accion):
    ip = ip_entry.get()
    if not ip:
        messagebox.showwarning("Advertencia", "Por favor, ingrese una dirección IP.")
        return
    
    if accion == "ping":
        pingre(ip)
    elif accion == "bloquear":
        bloquear_ping_desde_ip(ip)
    elif accion == "permitir":
        permitir_ping_desde_ip(ip)

# Configuración de la interfaz gráfica
root = tk.Tk()
root.title("Menú de Ping para macOS")

tk.Label(root, text="Ingrese la dirección IP:").pack(pady=5)
ip_entry = tk.Entry(root)
ip_entry.pack(pady=5)

ping_button = tk.Button(root, text="Realizar Ping", command=lambda: realizar_accion("ping"))
ping_button.pack(pady=5)

bloquear_button = tk.Button(root, text="Bloquear Ping desde IP", command=lambda: realizar_accion("bloquear"))
bloquear_button.pack(pady=5)

permitir_button = tk.Button(root, text="Permitir Ping desde IP", command=lambda: realizar_accion("permitir"))
permitir_button.pack(pady=5)

resultado_text = tk.Text(root, height=10, width=50)
resultado_text.pack(pady=10)

root.mainloop()