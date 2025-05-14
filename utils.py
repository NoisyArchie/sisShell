"""Este modulo contiene las funciones para obtener la información correspondiente
a cada comando. se deben de ir agregando las funciones para obtener la información
para cada comando que se implemente.
faltan: usodisco, usodicodet, graficadico, gdd, exportar."""
import os
import platform
import psutil
import datetime
import subprocess
import sys

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

#Memoria detallada
def memdetallada():
    """Devuelve el uso detallado de memoria RAM y Swap en GB"""
    mem = psutil.virtual_memory()
    swap = psutil.swap_memory()
    return {
        "RAM": {
            "Total": f"{mem.total / (1024**3):.2f} GB",
            "Disponible": f"{mem.available / (1024**3):.2f} GB",
            "Usada": f"{mem.used / (1024**3):.2f} GB",
            "Porcentaje": f"{mem.percent}%"
        },
        "Swap": {
            "Total": f"{swap.total / (1024**3):.2f} GB",
            "Usado": f"{swap.used / (1024**3):.2f} GB",
            "Porcentaje": f"{swap.percent}%"
        }
    }

#CPU cores 
def cpucores():
    """Devuelve el porcentaje de uso por cada núcleo del CPU"""
    cores = psutil.cpu_percent(percpu=True)
    return {f"Núcleo {i}": f"{core}%" for i, core in enumerate(cores, 1)}

#Ping local
def pinglocal():
    """Realiza un ping a localhost y devuelve el resultado"""
    param = "-n" if platform.system().lower() == "windows" else "-c"
    try:
        output = subprocess.run(
            ["ping", param, "4", "127.0.0.1"],
            capture_output=True,
            text=True,
            timeout=10  # Evita bloqueos
        )
        return output.stdout if output.returncode == 0 else "Error en ping"
    except Exception as e:
        return f"Error: {str(e)}"
    
#Salir
def salir():
    """Cierra la aplicación de manera segura"""
    print("Cerrando aplicación...")
    sys.exit(0)  # Libera recursos y llama a os._exit() internamente

#Uso de cpu y ram
def recursos():
    """Devuelve el uso global de CPU y RAM"""
    return {
        "CPU": f"{psutil.cpu_percent()}%",
        "RAM": f"{psutil.virtual_memory().percent}%",
        "Núcleos físicos": psutil.cpu_count(logical=False),
        "Núcleos lógicos": psutil.cpu_count()
    }

#Top 5 procesos
def top5():
    """Devuelve los 5 procesos que más CPU y RAM consumen"""
    procesos = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        try:
            procesos.append(proc.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    
    # Ordena y selecciona top 5
    top_cpu = sorted(procesos, key=lambda p: p['cpu_percent'], reverse=True)[:5]
    top_mem = sorted(procesos, key=lambda p: p['memory_percent'], reverse=True)[:5]
    
    return {
        "Top 5 CPU": [{p['name']: f"{p['cpu_percent']}%"} for p in top_cpu],
        "Top 5 RAM": [{p['name']: f"{p['memory_percent']}%"} for p in top_mem]
    }

def ayuda():
    return {
        "miinfo": "Muestra información básica del sistema.",
        "limpiar": "Limpia la pantalla del shell.",
        "hora": "Muestra la hora actual.",
        "fecha": "Muestra la fecha actual.",
        "listar": "Lista archivos del directorio actual.",
        "memdetallada": "Muestra el uso detallado de la memoria.",
        "cpucores": "Muestra uso del CPU por núcleo.",
        "pinglocal": "Ejecuta ping a localhost.",
        "salir": "Cierra el programa.",
        "ayuda": "Muestra esta lista de comandos personalizados.",
        "recursos": "Muestra uso actual de CPU y RAM.",
        "top5": "Muestra los 5 procesos con más uso de CPU/RAM.",
        "usodisco": "Muestra el uso de disco principal.",
        "usodiscodet": "Muestra el uso de todas las particiones del disco.",
        "graficadisco": "Muestra una gráfica circular del uso de disco.",
        "gdd": "Muestra una gráfica detallada del uso por partición.",
        "exportar <archivo.txt>": "Exporta la salida del shell a un archivo de texto."
    }

def usodisco():
    disco_principal = "/"
    if platform.system() == "Windows":
        disco_principal = os.path.splitdrive(os.getcwd())[0] + "\\"
    elif platform.system() == "Linux":
        disco_principal = "/"

    uso = psutil.disk_usage(disco_principal)
    
    resultado = (
        f"Disco en: {disco_principal}\n"
        f"Total: {round(uso.total / (1024**3), 2)} GB\n"
        f"Usado: {round(uso.used / (1024**3), 2)} GB\n"
        f"Libre: {round(uso.free / (1024**3), 2)} GB\n"
        f"Porcentaje usado: {uso.percent}%\n"
    )
    return resultado