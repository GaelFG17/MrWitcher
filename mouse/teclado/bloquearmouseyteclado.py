import paramiko

def bloquear_teclado_remoto(hostname, port, username, password):
    try:
        # Crear una instancia de SSHClient
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        # Conectar al host remoto
        client.connect(hostname, port=port, username=username, password=password)
        
        # Comando para bloquear el teclado
        comando = "xinput float $(xinput list --id-only 'AT Translated Set 2 keyboard')"
        
        # Ejecutar el comando en la máquina remota
        stdin, stdout, stderr = client.exec_command(comando)
        
        # Leer la salida y los errores
        salida = stdout.read().decode()
        errores = stderr.read().decode()
        
        # Cerrar la conexión
        client.close()
        
        return salida, errores
    except Exception as e:
        return str(e)

# Ejemplo de uso
hostname = '192.168.10.42'
port = 22
username = 'JULY'
password = '1234'

salida, errores = bloquear_teclado_remoto(hostname, port, username, password)
print("Salida:", salida)
print("Errores:", errores)