import paramiko

# Establecer conexión SSH
hostname = '192.168.174.1'
username = 'Manuel Arce'
password = '210191'

# Crear cliente SSH
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(hostname, username=username, password=password)

# Ejecutar el script para bloquear el teclado
stdin, stdout, stderr = client.exec_command('python3 C:/Users/Manuel Arce/Documents/Chemin/script.py')

# Leer los resultados (si es necesario)
print(stdout.read().decode())

# Cerrar la conexión SSH
client.close()
