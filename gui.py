##Archivo de interfaz grafica en donde se le da estilo a los frames del programa
import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog
from shell import Shell
from commands import Commands
from utils import get_current_path
import psutil
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.patheffects as patheffects

class CustomShellUI:
    def __init__(self, root):
        self.root = root
        self.root.title("SisShell")
        self.root.geometry("900x650")
        self.root.minsize(700, 500)
        self.create_system_stats()  
        self.create_resource_graphs()  
        self.update_metrics()  
        
        # Configuración del tema 
        self.set_neon_theme()
        
        # Objeto shell y comandos
        self.shell = Shell(self)
        self.commands = Commands(self.shell)
        
        # Barra de ruta
        self.path_frame = ttk.Frame(self.root, style='Neon.TFrame')
        self.path_frame.pack(fill=tk.X, padx=10, pady=(10, 0))
        
        self.current_path = get_current_path()
        self.path_label = ttk.Label(
            self.path_frame,
            text=self.current_path,
            font=('Consolas', 10, 'bold'),
            style='Neon.TLabel',
            relief=tk.GROOVE,
            padding=5
        )
        self.path_label.pack(fill=tk.X, expand=True)
        
        # Terminal principal con su scroll
        self.main_frame = ttk.Frame(self.root, style='Neon.TFrame')
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.text_output = scrolledtext.ScrolledText(
            self.main_frame,
            wrap=tk.WORD,
            bg='#0a0a12',
            fg='#00fffc',
            insertbackground='#ff00ff',
            selectbackground='#6a00ff',
            selectforeground='#ffffff',
            font=('Consolas', 12),
            padx=15,
            pady=15,
            state="normal",
            highlightthickness=2,
            highlightbackground='#6a00ff'
        )
        self.text_output.pack(fill=tk.BOTH, expand=True)
        
        # Panel de entrada de comandos
        self.input_frame = ttk.Frame(self.root, style='Neon.TFrame')
        self.input_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        # Prompt con estilo neon
        self.prompt_label = ttk.Label(
            self.input_frame,
            text=">",
            font=('Consolas', 14, 'bold'),
            style='NeonPrompt.TLabel',
            padding=(0, 0, 10, 0)
        )
        self.prompt_label.pack(side=tk.LEFT)
        
        # Entrada de comandos
        self.command_entry = ttk.Entry(
            self.input_frame,
            font=('Consolas', 12),
            style='Neon.TEntry',
            width=50
        )
        self.command_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))

        #Botón para exportar la salida a un archivo.
        self.export_button = ttk.Button(
            self.input_frame,
            text = "Exportar",
            style = 'Neon.TButton',
            command=lambda: self.export_output()
        )
        self.export_button.pack(side=tk.RIGHT)

        # Botón de ejecución
        self.run_button = ttk.Button(
                self.input_frame,
                text="Ejecutar",
                style='Neon.TButton',
                command=lambda: self.execute_command(None)
            )  # <-- Paréntesis cerrado aquí
        self.run_button.pack(side=tk.RIGHT)

        # Eventos (sin cambios)
        self.command_entry.bind("<Return>", self.execute_command)
        self.command_entry.bind("<Up>", self.show_previous_command)
        self.command_entry.bind("<Down>", self.show_next_command)
        self.command_entry.focus_set()
        
        # Historial (sin cambios)
        self.command_history = []
        self.history_index = -1
        
        # Mensaje de bienvenida
        self.display_welcome_message()
        
    def create_system_stats(self):
        """Sección de estadísticas en tiempo real debajo de la entrada"""
        self.stats_frame = ttk.Frame(self.root, style='Neon.TFrame')
        self.stats_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=(0, 5))
    
        # Variables dinámicas
        self.cpu_var = tk.StringVar(value="🖥 CPU: 0.0%")
        self.ram_var = tk.StringVar(value="💾 RAM: 0.0%")
        self.disk_var = tk.StringVar(value="💿 DISK: 0.0%")
    
        # Estilo común
        stat_style = {
            'style': 'Neon.TLabel',
            'font': ('Consolas', 10, 'bold'),
            'padding': (15, 8),
            'anchor': tk.CENTER
        }
    
        # Etiquetas para estadisticas
        ttk.Label(self.stats_frame, textvariable=self.cpu_var, 
                 foreground='#00fffc', **stat_style).pack(side=tk.LEFT, expand=True)
    
        ttk.Label(self.stats_frame, textvariable=self.ram_var,
                 foreground='#ff00ff', **stat_style).pack(side=tk.LEFT, expand=True)
    
        ttk.Label(self.stats_frame, textvariable=self.disk_var,
                 foreground='#6a00ff', **stat_style).pack(side=tk.LEFT, expand=True)

    def create_resource_graphs(self):
        """Gráficos circulares para recursos del sistema"""
        self.graph_frame = ttk.Frame(self.root, style='Graph.TFrame')
        self.graph_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=10, pady=10, expand=True)
    
        # Configuración del frae de las estadfisticas
        self.graph_style = {
            'figsize': (1.75, 1.25),
            'facecolor': '#0a0a12',
            'edgecolor': '#6a00ff',
            'dpi': 90
        }
    
        # Creacion de graficos
        self.cpu_fig = Figure(**self.graph_style)
        self.cpu_ax = self.cpu_fig.add_subplot(111)
        self.cpu_canvas = FigureCanvasTkAgg(self.cpu_fig, self.graph_frame)
        self.cpu_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
        self.ram_fig = Figure(**self.graph_style)
        self.ram_ax = self.ram_fig.add_subplot(111)
        self.ram_canvas = FigureCanvasTkAgg(self.ram_fig, self.graph_frame)
        self.ram_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def update_resource_graph(self, ax, value, color):
        """Actualiza los gráficos circulares"""
        ax.clear()
        ax.pie([value, 100-value], 
              colors=[color, '#1a1a2f'],
              startangle=90,
              wedgeprops={'linewidth': 1.5, 'edgecolor': '#6a00ff'})
        ax.text(0, 0, f"{value:.1f}%", 
              ha='center', va='center', 
              fontsize=14, color=color,
              path_effects=[patheffects.withStroke(linewidth=3, foreground='#0a0a12')])

    def update_metrics(self):
        """Actualiza todas las métricas del sistema"""
        try:
            # Obtener datos de la computadora 
            cpu = psutil.cpu_percent()
            ram = psutil.virtual_memory().percent
            disk = psutil.disk_usage('/').percent
        
            # Actualizar los dats
            self.cpu_var.set(f"🖥 CPU: {cpu:.1f}%")
            self.ram_var.set(f"💾 RAM: {ram:.1f}%")
            self.disk_var.set(f"💿 ALMACENAMIENTO: {disk:.1f}%")
        
            # Actualizar los gráficos
            self.update_resource_graph(self.cpu_ax, cpu, '#00fffc')
            self.update_resource_graph(self.ram_ax, ram, '#ff00ff')
            self.cpu_canvas.draw_idle()
            self.ram_canvas.draw_idle()
        
        except Exception as e:
            print(f"Error en métricas: {str(e)}")
    
        self.root.after(1000, self.update_metrics)
    
    def set_neon_theme(self):
        """Configura el tema neon futurista"""
        self.root.configure(bg='#0a0a12')
        
        # Configurar colores 
        self.neon_blue = '#4db8ff'
        self.neon_pink = '#ff00ff'
        self.neon_purple = '#6a00ff'
        self.dark_bg = '#0a0a12'
        self.darker_bg = '#050510'
        
        # Configurar estilos ttk
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        #Estilos de las graficas
        self.style.configure('Graph.TFrame', 
                       background='#12012a',
                       borderwidth=2,
                       relief='ridge',
                       lightcolor=self.neon_purple,
                       darkcolor='#12012a')
        
        
        
        # Frame style
        self.style.configure('Neon.TFrame', background=self.dark_bg)
        
        # Label style
        self.style.configure('Neon.TLabel', 
                           background=self.darker_bg, 
                           foreground=self.neon_blue,
                           bordercolor=self.neon_purple,
                           lightcolor=self.neon_purple,
                           darkcolor=self.darker_bg)
        
        # Prompt style
        self.style.configure('NeonPrompt.TLabel',
                           background=self.dark_bg,
                           foreground=self.neon_pink,
                           font=('Consolas', 14, 'bold'))
        
        # Entry style
        self.style.configure('Neon.TEntry',
                           fieldbackground=self.darker_bg,
                           foreground=self.neon_blue,
                           bordercolor=self.neon_purple,
                           lightcolor=self.neon_purple,
                           darkcolor=self.darker_bg,
                           insertwidth=2)
        
        # Button style
        self.style.configure('Neon.TButton',
                           background=self.darker_bg,
                           foreground=self.neon_pink,
                           bordercolor=self.neon_purple,
                           lightcolor=self.neon_purple,
                           darkcolor=self.darker_bg,
                           font=('Consolas', 10, 'bold'),
                           padding=5)
        self.style.map('Neon.TButton',
                     background=[('active', '#12012a')],
                     foreground=[('active', self.neon_blue)])
    
    def display_welcome_message(self):
        """Muestra mensaje de bienvenida con estilo futurista"""
        welcome_msg = """
╔══════════════════════════════════════════════════════╗
║                   ⢀⣤⣤⣤⣄⣀⣠⣤⣤⣄⡀                    
║                 ⣰⠟⠁⠀⠀⠀⠉⠉⠀⠀⠀⠈⠛⢷⡄                 
║              ⢀⣴⠾⠃⠀⠀⣾⣿⣷⡄⠀⢠⣾⣿⣷⡄⠈⣿⣤⣄⡀              
║             ⢰⡟⠁⠀⣀⡀⠘⣿⣿⣿⡇⠀⢸⣿⣿⣿⠃⠀⠀⠀⠈⢻⣆             
║             ⣿⡇⠀⣼⣿⣿⡄⠈⠛⠛⠁⠀⠀⠙⠉⠁⠀⣠⣶⣦⡀⠀⣿            
║             ⣿⡇⠀⠸⣿⣿⠇⠀⠀⣠⣾⣿⣿⣦⠀⠀⢸⣿⣿⣿⠇⠀⣿             
║             ⢸⣇⠀⠀⠈⠁⠀⣠⣶⣿⣿⣿⣿⣿⣧⣄⠈⠛⠛⠋⠀⣼⠃             
║              ⢿⡄⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⣼⡏              
║               ⠈⣿⡀⠀⠀⠈⠻⠿⠟⠛⠛⠻⠿⠿⠟⠃⠀⢸⣿             
║                ⣽⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡟               
║                ⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡇               
╠══════════════════════════════════════════════════════╣
║       SisShell - Escribe 'ayuda' para más info       ║
╚══════════════════════════════════════════════════════╝

"""
        self.text_output.insert(tk.END, welcome_msg, 'neon_pink')
        self.text_output.tag_config('neon_pink', foreground=self.neon_pink)
        self.text_output.insert(tk.END, f"\n\n{self.current_path} ", 'path_style')
        self.text_output.tag_config('path_style', foreground=self.neon_blue)
        self.text_output.insert(tk.END, ">>> ", 'prompt_style')
        self.text_output.tag_config('prompt_style', foreground=self.neon_pink)
        self.text_output.see(tk.END)

    #Actualizar laber de la ruta actual.
    def update_path_label(self):
        self.current_path = get_current_path()
        self.path_label.config(text=self.current_path)
    
    # MÉTODOS ORIGINALES (SIN MODIFICACIONES)
    def execute_command(self, event=None):
        self.text_output.config(state="normal")
        command = self.command_entry.get()
        
        # Mostrar comando con estilo diferente
        self.text_output.insert(tk.END, "> ", 'prompt_style')
        self.text_output.insert(tk.END, f"{command}\n", 'command_style')
        self.text_output.tag_config('command_style', foreground='#ffffff')
        
        self.command_history.append(command)
        self.history_index = len(self.command_history)
        self.shell.execute(command)
        
        # Separador entre comandos
        self.text_output.insert(tk.END, "-"*80 + "\n", 'separator')
        self.text_output.tag_config('separator', foreground=self.neon_purple)
        
        self.text_output.see("end")
        self.text_output.config(state="disabled")
        self.command_entry.delete(0, tk.END)

    def show_previous_command(self, event=None):
        if self.command_history and self.history_index > 0:
            self.history_index -= 1
            self.command_entry.delete(0, tk.END)
            self.command_entry.insert(0, self.command_history[self.history_index])
        return "break"

    def show_next_command(self, event=None):
        if self.command_history and self.history_index < len(self.command_history) - 1:
            self.history_index += 1
            self.command_entry.delete(0, tk.END)
            self.command_entry.insert(0, self.command_history[self.history_index])
        else:
            self.history_index = len(self.command_history)
            self.command_entry.delete(0, tk.END)
        return "break"

    def export_output(self):
        content = self.text_output.get("1.0", tk.END)
    
        file_path = tk.filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")],
            title="Exportar salida"
        )
        
        if file_path:  # Si el usuario no cancela
            try:
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write(content)
                self.text_output.insert(tk.END, f"\nSalida exportada a: {file_path}\n", 'success')
            except Exception as e:
                self.text_output.insert(tk.END, f"\nError al exportar: {str(e)}\n", 'error')
        self.text_output.see(tk.END)