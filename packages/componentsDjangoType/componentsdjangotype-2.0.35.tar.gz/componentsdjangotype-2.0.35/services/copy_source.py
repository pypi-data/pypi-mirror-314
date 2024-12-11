import os
import shutil
import sys

def copy_static_file(source_path, destination_path, stdout=sys.stdout):
    """
    Copia un archivo estático (HTML, CSS, JS) a una ruta de destino.

    :param source_path: Ruta completa del archivo fuente.
    :param destination_path: Ruta completa del archivo destino.
    :param stdout: Salida estándar para mensajes (por defecto usa sys.stdout).
    """
    try:
        # Verificar si el archivo fuente existe
        if not os.path.exists(source_path):
            stdout.write(f"El archivo fuente '{source_path}' no existe.\n")
            return

        # Crear el directorio de destino si no existe
        os.makedirs(os.path.dirname(destination_path), exist_ok=True)

        # Verificar si el archivo de destino ya existe
        if os.path.exists(destination_path):
            stdout.write(f"El archivo '{destination_path}' ya existe.\n")
            return

        # Copiar el archivo al destino
        shutil.copy(source_path, destination_path)
        stdout.write(f"El archivo '{source_path}' fue copiado a '{destination_path}'.\n")

    except Exception as e:
        stdout.write(f"Error al copiar el archivo: {e}\n")