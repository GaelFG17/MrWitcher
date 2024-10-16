from pynput.keyboard import Controller, Listener

# Función para bloquear el teclado
def block_key(key):
    # Aquí puedes agregar condiciones específicas si deseas bloquear teclas específicas
    return False  # Esto evita que las teclas sean presionadas

# Iniciar el listener para el teclado
with Listener(on_press=block_key) as listener:
    listener.join()
