import importlib.resources as pkg_resources
import shutil
import os
import sys

def copy_static_file(package, resource_name, destination_path, stdout=sys.stdout):
    """
    Copia un archivo estático empaquetado a una ruta de destino.

    :param package: El nombre del paquete donde está el recurso.
    :param resource_name: Ruta relativa del recurso dentro del paquete.
    :param destination_path: Ruta completa donde se copiará el archivo.
    :param stdout: Salida estándar para mensajes (por defecto usa sys.stdout).
    """
    try:
        # Verifica si el recurso existe en el paquete
        if not pkg_resources.is_resource(package, resource_name):
            stdout.write(f"El recurso '{resource_name}' no existe en el paquete '{package}'.\n")
            return

        # Crear el directorio de destino si no existe
        os.makedirs(os.path.dirname(destination_path), exist_ok=True)

        # Leer el archivo desde el paquete y escribirlo en la ruta destino
        with pkg_resources.open_binary(package, resource_name) as resource_file:
            with open(destination_path, 'wb') as dest_file:
                shutil.copyfileobj(resource_file, dest_file)

        stdout.write(f"El recurso '{resource_name}' fue copiado a '{destination_path}'.\n")
    except Exception as e:
        stdout.write(f"Error al copiar el archivo: {e}\n")