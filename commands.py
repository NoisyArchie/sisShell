"""Este archivo contiene la clase que maneja los comandos del shell.
se deben de ir agregando los metodos para cada comando que se implemente
Pendientes de revision: memdetallada, cpucores, pinglocal, salir, ayuda, recursos, top5, usodisco, usodicodet, graficadico, gdd, exportar

faltan: Los comandos extras naturales sin personalizar - Contemplar y garantizar al menos
10 comandos externos reales (naturales del SO) que operen dentro del Shell, es decir, que
no estén en la lista de comandos extendidos personalizados
(dir, ping, ipconfig, tasklist, calc, notepad, ls etc.)."""
import subprocess
import threading
from utils import system_info, show_time, show_date, list_files, memdetallada, cpucores, pinglocal, salir, recursos, top5, ayuda, usodisco, usodiscodet, graficadisco, gdd, exportar_salida, mover_dir, regresar, cumple #del archivo utils.py vamos agregando las nuevas funciones aki

class Commands:
    def __init__(self, shell):
        self.shell = shell
        self.commands_dict = {
            "miinfo": self.system_info,
            "limpiar": self.clear_output,
            "hora": self.show_time,
            "fecha": self.show_date,
            "listar": self.list_files,
            "memdetallada": self.memdetallada,
            "cpucores": self.cpucores,
            "pinglocal": self.pinglocal,
            "salir": self.salir,
            "ayuda": self.ayuda,
            "recursos": self.recursos,
            "top5": self.top5,
            "usodisco": self.usodisco,
            "usodiscodet": self.usodiscodet,
            "graficadisco": self.graficadisco,
            "gdd": self.gdd,
            "exportar": self.exportar,
            "mover": self.mover,
            "regresar": self.regresar,
            "cumple": self.cumpleaños,
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
        self.shell.ui.display_welcome_message()

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

    def memdetallada(self):
        try:
            mem = memdetallada()
            self.shell.ui.text_output.insert("end", "=== MEMORIA DETALLADA ===\n")
            for key, value in mem.items():
                self.shell.ui.text_output.insert("end", f"{key}: {value}\n")
        except Exception as e:
            self.shell.ui.text_output.insert("end", f"Error al obtener información de memoria: {e}\n")

    def cpucores(self):
        try:
            cores = cpucores()
            self.shell.ui.text_output.insert("end", "=== USO DE CPU POR NÚCLEO ===\n")
            for key, value in cores.items():
                self.shell.ui.text_output.insert("end", f"{key}: {value}\n")
        except Exception as e:
            self.shell.ui.text_output.insert("end", f"Error al obtener información de CPU: {e}\n")

    def pinglocal(self):
        try:
            output = pinglocal()
            self.shell.ui.text_output.insert("end", "=== RESULTADO DEL PING A LOCALHOST ===\n")
            self.shell.ui.text_output.insert("end", output)
        except Exception as e:
            self.shell.ui.text_output.insert("end", f"Error al realizar el ping: {e}\n")

    def salir(self):
        self.shell.ui.text_output.insert("end", "Saliendo del programa...\n")
        salir()
        
    def recursos(self):
        try:
            recursos_info = recursos()
            self.shell.ui.text_output.insert("end", "=== RECURSOS DEL SISTEMA ===\n")
            for key, value in recursos_info.items():
                self.shell.ui.text_output.insert("end", f"{key}: {value}\n")
        except Exception as e:
            self.shell.ui.text_output.insert("end", f"Error al obtener información de recursos: {e}\n")

    def top5(self):
        try:
            top5_info = top5()
            self.shell.ui.text_output.insert("end", "=== TOP 5 PROCESOS ===\n")
            for key, value in top5_info.items():
                self.shell.ui.text_output.insert("end", f"{key}: {value}\n")
        except Exception as e:
            self.shell.ui.text_output.insert("end", f"Error al obtener información de procesos: {e}\n")

    def ayuda(self):
        try:
            info_ayuda = ayuda()
            self.shell.ui.text_output.insert("end", "=== AYUDA -COMANDOS DISPONIBLES ===\n")
            for key, value in info_ayuda.items():
                self.shell.ui.text_output.insert("end", f"{key}: {value}\n")
        except Exception as e:
            self.shell.ui.text_output.insert("end", f"Error al obtener información de ayuda: {e}\n")

    def usodisco(self):
        try:
            uso_disco = usodisco()
            self.shell.ui.text_output.insert("end", "=== USO DEL DISCO ===\n")
            self.shell.ui.text_output.insert("end", uso_disco + "\n")
        except Exception as e:
            self.shell.ui.text_output.insert("end", f"Error al obtener información del disco: {e}\n")

    def usodiscodet(self):
        try:
            detalles_disco = usodiscodet()
            self.shell.ui.text_output.insert("end", "=== DETALLES DE TODAS LAS PARTICIONES DEL DISCO ===\n")
            self.shell.ui.text_output.insert("end", detalles_disco + "\n")
        except Exception as e:
            self.shell.ui.text_output.insert("end", f"Error al obtener información del disco: {e}\n")

    def graficadisco(self):
        try:
            self.shell.ui.text_output.insert("end", "Generando gráfica del uso del disco...\n")
            graficadisco()
        except Exception as e:
            self.shell.ui.text_output.insert("end", f"Error al obtener graficar disco disco: {e}\n")

    def gdd(self):
        try:
            self.shell.ui.text_output.insert("end", "Generando gráfica detallada del disco...\n")
            errores = gdd()
            if errores:
                for error in errores:
                    self.shell.ui.text_output.insert("end", f"{error}\n")
        except Exception as e:
            self.shell.ui.text_output.insert("end", f"Error al generar la gráfica detallada: {e}\n")

    def exportar(self, nombre = None):
        try:
            if not nombre:
                self.shell.ui.text_output.insert("end", "Debes insertar un nombre para el archivo.\n")
                return
            
            if not nombre.lower().endswith(".txt"):
                nombre += ".txt"
            
            contenido = self.shell.ui.text_output.get("1.0", "end-1c")
            mensaje = exportar_salida(contenido, nombre)
            self.shell.ui.text_output.insert("end", f"{mensaje}\n")
        except Exception as e:
            self.shell.ui.text_output.insert("end", f"Error al exportar: {e}\n")

    def mover(self, ruta):
        result = mover_dir(ruta)
        self.shell.ui.update_path_label()
        self.shell.ui.text_output.insert("end", result)

    def regresar(self):
        result = regresar()
        self.shell.ui.update_path_label()
        self.shell.ui.text_output.insert("end", result)

    def cumpleaños(self):
        try:
            self.shell.ui.text_output.insert("end", "🎉 ¡Feliz cumpleaños! 🎂\n")
            self.shell.ui.text_output.insert("end", "Reproduciendo sorpresa musical... 🎶\n")

            # Reproducir el audio en segundo plano
            hilo_audio = threading.Thread(target=cumple)
            hilo_audio.start()

        except Exception as e:
            self.shell.ui.text_output.insert("end", f"Error al activar cumpleaños: {e}\n")
            
#aqui continuamos con los métodos para los comandos porfo

    def execute_external_command(self, command):
        try:
            result = subprocess.run(command, shell = True, capture_output = True)
            self.shell.ui.text_output.insert("end", result.stdout)
        except Exception as e:
            self.shell.ui.text_output.insert("1.0", f"Error al ejecutar el comando: {e}\n")