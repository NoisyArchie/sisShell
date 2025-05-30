"""Este modulo contiene las funciones para obtener la información correspondiente
a cada comando. se deben de ir agregando las funciones para obtener la información
para cada comando que se implemente.
faltan: Los comandos extras naturales sin personalizar - Contemplar y garantizar al menos
10 comandos externos reales (naturales del SO) que operen dentro del Shell, es decir, que
no estén en la lista de comandos extendidos personalizados
(dir, ping, ipconfig, tasklist, calc, notepad, ls etc.).
."""
import os
import platform
import psutil
import datetime
import subprocess
import sys
import matplotlib.pyplot as plt
import pygame

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

#aiuda
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
        "exportar <archivo.txt>": "Exporta la salida del shell a un archivo de texto.",
        "mover <nombre_carpeta>": "Mueve hacia un directorio dentro de la ruta.",
        "regresar": "regresa a un hacia un directorio anterior.",
        ":== COMANDOS NATIVOS ==": "",
        "ipconfig": "Muestra las direcciones del protocolo de Internet, máscara de subred y puerta de enlace predeterminada.",
        "mkdir <nombre>": "Crea un directorio.",
        "rmdir <nombre>": "Elimina un directorio",
        "tree": "Muestra la estructura de directorios de una ruta",
        "vol": "Muestra la etiqueta del volumen y el número de serie del disco.",
        "tasklist": "Muestra todas las tareas en ejecución, incluidos los servicios.",
        "type <nombre_archivo>": "Muestra el contenido de una rchivo de texto.",
        "ver": "Muestra la versión de Windows.",
        "gpresult": "Muestra información de directiva de grupo por equipo o usuario.",
        "driverquery": "Muestra el estado y las propiedades actuales del controlador de dispositivo."
    }

#usodeldisco
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

#uso de cada partición del disco (si existe)
def usodiscodet():
    particiones = psutil.disk_partitions()
    resultados = []

    for particion in particiones:
        try:
            uso = psutil.disk_usage(particion.mountpoint)
            resultados.append(
                f"Partición: {particion.device}\n"
                f"  Punto de montaje: {particion.mountpoint}\n"
                f"  Tipo de sistema de archivos: {particion.fstype}\n"
                f"  Total: {round(uso.total / (1024**3), 2)} GB\n"
                f"  Usado: {round(uso.used / (1024**3), 2)} GB\n"
                f"  Libre: {round(uso.free / (1024**3), 2)} GB\n"
                f"  Porcentaje usado: {uso.percent}%\n"
                "----------------------------------------\n"
            )
        except PermissionError:
            resultados.append(
                f"Partición: {particion.device} \n ACCESO DENEGADO.\n"
                "----------------------------------------\n"
            )
        return "".join(resultados)
    
def graficadisco():
    if platform.system().lower() == "windows":
        disco = os.path.splitdrive(os.getcwd())[0] + "\\"
    else:
        disco = "/"

    # Obtener uso del disco
    uso = psutil.disk_usage(disco)

    labels = ['Usado', 'Libre']
    values = [uso.used, uso.free]
    colores = ["#ff00ff", "#6a00ff"] 

    
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(7, 7), facecolor='#121212')
    wedges, texts, autotexts = ax.pie(
        values, labels=labels, colors=colores, autopct='%1.1f%%',
        startangle=140, textprops=dict(color='white'), wedgeprops=dict(width=0.4)
    )

    for text in texts:
        text.set_fontsize(12)
    for autotext in autotexts:
        autotext.set_fontsize(13)
        autotext.set_color('#ffffff')

    ax.set_title('Uso del Disco', fontsize=16, color='white')
    ax.axis('equal')
    plt.tight_layout()
    plt.show()

def gdd():
    particiones = psutil.disk_partitions(all=False)
    labels = []
    porcentajes = []
    errores = []

    for p in particiones:
        try:
            uso = psutil.disk_usage(p.mountpoint)
            labels.append(p.device)
            porcentajes.append(uso.used)
        except Exception as e:
            errores.append(f"No se pudo acceder a {p.device}: {e}")

    if not labels:
        raise Exception("No se pudo obtener información de las particiones.")

    
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(8, 8), facecolor='#121212')

    
    colores_neon = ["#991df2", '#ff00ff', '#39ff14', '#fffb00', '#ff6ec7', '#6a00ff']


    colores = colores_neon * ((len(labels) // len(colores_neon)) + 1)

    wedges, texts, autotexts = ax.pie(
        porcentajes, labels=labels, colors=colores[:len(labels)],
        autopct='%1.1f%%', startangle=140, textprops=dict(color='white'),
        wedgeprops=dict(width=0.4)
    )

    for text in texts:
        text.set_fontsize(11)
    for autotext in autotexts:
        autotext.set_fontsize(12)
        autotext.set_color('white')

    ax.set_title("Uso de Disco por Partición", fontsize=16, color='white')
    ax.axis('equal')
    plt.tight_layout()
    plt.show()

    return errores

def exportar_salida(contenido, nombre):
    try:
        with open(nombre, "w", encoding = "utf-8") as archivo:
            archivo.write(contenido)
        return f"Salida exportada correctamente en '{nombre}'"
    except Exception as e:
        return f"Error al exportar el archivo {e}"

historial_rutas = []
def mover_dir(ruta):
    if os.path.isdir(ruta):
        historial_rutas.append(os.getcwd())
        os.chdir(ruta)
        return f"Movido a {os.getcwd()}"
    else:
        return f"No se pudo mover a {ruta} o el directorio no existe..."

def regresar():
    if not historial_rutas:
        return "No hay carpeta anterior a la que regresar."
    
    ruta_anterior = historial_rutas.pop()
    try:
        os.chdir(ruta_anterior)
        return(f"Regresado a: {os.getcwd()}")
    except Exception as e:
        return(f"Error al regresar: {e}")

def cumple():
    try:
        pygame.mixer.init()
        pygame.mixer.music.load("secret.wav")
        pygame.mixer.music.play()
    except Exception as e:
        print(f"Error al reproducir el audio: {e}")
