"""Este modulo contiene las funciones para obtener la información correspondiente
a cada comando. se deben de ir agregando las funciones para obtener la información
para cada comando que se implemente.
faltan: memdatallada, cpucores, pinglocal, salir, ayuda, recursos, top5,
usodisco, usodicodet, graficadico, gdd, exportar."""
import os
import platform
import psutil
import datetime

def get_current_path():
    return os.getcwd()

def system_info():
    info = {
        "Sistema": platform.system(),
        "Nombre del sistema": platform.node(),
        "Versión del sistema": platform.version(),
        "Arquitectura": platform.architecture()[0],
        "Procesador": platform.processor(),
        "Memoria Ram:": f"{psutil.virtual_memory().total / (1024**3):.2f} GB",
        "CPU": f"{psutil.cpu_percent()}% uso",
    }
    return info

def show_time():
    return datetime.datetime.now().strftime("%H:%M:%S")

def show_date():
    return datetime.datetime.now().strftime("%d/%m/%Y")

def list_files(path):
    return os.listdir(path)