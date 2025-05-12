"""Este archivo contiene la clase que maneja los comandos del shell.
se deben de ir agregando los metodos para cada comando que se implemente
faltan: memdatallada, cpucores, pinglocal, salir, ayuda, recursos, top5,
usodisco, usodicodet, graficadico, gdd, exportar."""
import subprocess
from utils import system_info, show_time, show_date, list_files #del archivo utils.py vamos agregando las nuevas funciones aki

class Commands:
    def __init__(self, shell):
        self.shell = shell
        self.commands_dict = {
            "miinfo": self.system_info,
            "limpiar": self.clear_output,
            "hora": self.show_time,
            "fecha": self.show_date,
            "listar": self.list_files,
            #Aqui hay que agregar más comandos chabales
        }

    def system_info(self):
        try:
            info = system_info()
            self.shell.ui.text_output.insert("end", "=== INFORMACIÓN DEL SISTEMA ===\n")
            for key, value in info.items():
                self.shell.ui.text_output.insert("end", f"{key}: {value}\n")
        except Exception as e:
            self.shell.ui.text_output.insert("end", f"Error al obtener información del sistema: {e}\n")

    def clear_output(self):
        self.shell.ui.text_output.delete("1.0", "end")

    def show_time(self):
        current_time = show_time()
        self.shell.ui.text_output.insert("end", f"Hora actual: {current_time}\n")

    def show_date(self):
        current_date = show_date()
        self.shell.ui.text_output.insert("end", f"Fecha actual: {current_date}\n")

    def list_files(self):
        try:
            files = list_files(".")
            self.shell.ui.text_output.insert("end", "=== LISTA DE ARCHIVOS DEL DIRECTORIO ===\n")
            for file in files:
                self.shell.ui.text_output.insert("end", f"{file}\n")
        except Exception as e:
            self.shell.ui.text_output.insert("end", f"Error al listar los archivos: {e}\n")

#aqui continuamos con los métodos para los comandos porfo

    def execute_external_command(self, command):
        try:
            result = subprocess.run(command, shell = True, capture_output = True)
            self.shell.ui.text_output.insert("1.0", result.stdout)
        except Exception as e:
            self.shell.ui.text_output.insert("1.0", f"Error al ejecutar el comando: {e}\n")