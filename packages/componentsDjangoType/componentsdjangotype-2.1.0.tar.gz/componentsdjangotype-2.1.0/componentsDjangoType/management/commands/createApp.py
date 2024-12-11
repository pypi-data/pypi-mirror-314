import os
from django.core.management.base import BaseCommand
from services.authenticator_configurator import DjangoProjectManager

class Command(BaseCommand):
    help = 'Crea una aplicación llamada Home, estructura de carpetas y configura urls automáticamente en el proyecto especificado'

    def handle(self, *args, **kwargs):
        # Nombre de la aplicación a crear
        app_name = "Home"

        # Paso 1: Solicitar el nombre de la aplicación principal al usuario
        project_name = input(
            "Por favor, ingresa el nombre de la aplicación principal del proyecto: ")
        
        creation = DjangoProjectManager(app_name=app_name, project_name=project_name)

        # Paso 2: Crear la aplicación "Home" si no existe
        creation.create_app()

        # Agregar automáticamente 'Home' a INSTALLED_APPS
        creation.installed_app()

        # Paso 3: Crear el archivo urls.py en la aplicación "Home" si no existe
        creation.create_urls(self.stdout)

        # Paso 4: Crear la carpeta services y el archivo authentication.py en Home
        creation.creation_auth(self.stdout)

        # Paso 5: crea el urls.py y modifica el archivo views.py
        creation.create_views_urls(self.stdout)

        # Paso 6: Crear la carpeta templates y estatic y los archivos HTML CSS y JS
        creation.creation_utils(self.stdout)

        self.stdout.write(self.style.SUCCESS(
            "Comando ejecutado exitosamente."))
