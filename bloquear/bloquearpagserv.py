import paramiko
import tkinter as tk
from tkinter import messagebox

def bloquear_pagina_web(hostname, username, password, url):
    comando_bloquear = f'echo 127.0.0.1 {url} >> C:\\Windows\\System32\\drivers\\etc\\hosts'
    comando_limpiar_cache = 'ipconfig /flushdns'
    comando_verificar_hosts = 'type C:\\Windows\\System32\\drivers\\etc\\hosts'

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname, username=username, password=password)

    stdin, stdout, stderr = ssh.exec_command(comando_bloquear)
    print(stdout.read().decode(errors='ignore'))
    print(stderr.read().decode(errors='ignore'))

    stdin, stdout, stderr = ssh.exec_command(comando_limpiar_cache)
    print(stdout.read().decode(errors='ignore'))
    print(stderr.read().decode(errors='ignore'))

    stdin, stdout, stderr = ssh.exec_command(comando_verificar_hosts)
    print("Contenido del archivo hosts:")
    print(stdout.read().decode(errors='ignore'))
    print(stderr.read().decode(errors='ignore'))

    ssh.close()

def desbloquear_pagina_web(hostname, username, password, url):
    comando_desbloquear = f'powershell -Command "(Get-Content C:\\Windows\\System32\\drivers\\etc\\hosts) -notmatch \\"127.0.0.1 {url}\\" | Set-Content C:\\Windows\\System32\\drivers\\etc\\hosts"'
    comando_limpiar_cache = 'ipconfig /flushdns'
    comando_verificar_hosts = 'type C:\\Windows\\System32\\drivers\\etc\\hosts'

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname, username=username, password=password)

    stdin, stdout, stderr = ssh.exec_command(comando_desbloquear)
    print(stdout.read().decode(errors='ignore'))
    print(stderr.read().decode(errors='ignore'))

    stdin, stdout, stderr = ssh.exec_command(comando_limpiar_cache)
    print(stdout.read().decode(errors='ignore'))
    print(stderr.read().decode(errors='ignore'))

    stdin, stdout, stderr = ssh.exec_command(comando_verificar_hosts)
    print("Contenido del archivo hosts:")
    print(stdout.read().decode(errors='ignore'))
    print(stderr.read().decode(errors='ignore'))

    ssh.close()

def ejecutar_accion(accion):
    hostname = entry_hostname.get()
    username = entry_username.get()
    password = entry_password.get()
    url = entry_url.get()

    if accion == 'bloquear':
        bloquear_pagina_web(hostname, username, password, url)
        messagebox.showinfo("Resultado", "Página bloqueada correctamente.")
    elif accion == 'desbloquear':
        desbloquear_pagina_web(hostname, username, password, url)
        messagebox.showinfo("Resultado", "Página desbloqueada correctamente.")
    else:
        messagebox.showerror("Error", "Acción no reconocida. Por favor, introduce 'bloquear' o 'desbloquear'.")

# Crear la interfaz gráfica
root = tk.Tk()
root.title("Bloquear/Desbloquear Página Web")

tk.Label(root, text="IP del host:").grid(row=0, column=0, padx=10, pady=5)
entry_hostname = tk.Entry(root)
entry_hostname.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Nombre de usuario:").grid(row=1, column=0, padx=10, pady=5)
entry_username = tk.Entry(root)
entry_username.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Contraseña:").grid(row=2, column=0, padx=10, pady=5)
entry_password = tk.Entry(root, show='*')
entry_password.grid(row=2, column=1, padx=10, pady=5)

tk.Label(root, text="URL a bloquear/desbloquear:").grid(row=3, column=0, padx=10, pady=5)
entry_url = tk.Entry(root)
entry_url.grid(row=3, column=1, padx=10, pady=5)

btn_bloquear = tk.Button(root, text="Bloquear", command=lambda: ejecutar_accion('bloquear'))
btn_bloquear.grid(row=4, column=0, padx=10, pady=10)

btn_desbloquear = tk.Button(root, text="Desbloquear", command=lambda: ejecutar_accion('desbloquear'))
btn_desbloquear.grid(row=4, column=1, padx=10, pady=10)

root.mainloop()