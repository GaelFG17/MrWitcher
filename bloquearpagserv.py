import winrm

# Datos de conexión a la máquina remota
remote_host = "192.168.252.1"
username = "Manuel Arce"
password = "210191"

# Crear una sesión WinRM
session = winrm.Session(f'http://{remote_host}:5985/wsman', auth=(username, password))

# Comando para bloquear Facebook en el firewall
comando = 'netsh advfirewall firewall add rule name="Block Facebook" dir=out action=block remoteip=157.240.0.0/16'

# Ejecutar el comando
result = session.run_cmd(comando)

# Verificar el resultado
if result.status_code == 0:
    print("Regla del firewall creada exitosamente. Facebook ha sido bloqueado.")
else:
    print(f"Error al crear la regla del firewall: {result.std_err.decode()}")
