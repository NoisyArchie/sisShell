"""Interfaz gráfica con estilo neon moderno y mejor visualización de comandos"""
import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog
from shell import Shell
from commands import Commands
from utils import get_current_path

class CustomShellUI:
    def __init__(self, root):
        self.root = root
        self.root.title("NeonShell - Terminal Futurista")
        self.root.geometry("900x650")
        self.root.minsize(700, 500)
        
        # Configuración del tema neon
        self.set_neon_theme()
        
        # Objeto shell y comandos (sin cambios)
        self.shell = Shell(self)
        self.commands = Commands(self.shell)
        
        # Barra de ruta con estilo neon
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
        
        # Terminal principal con scroll
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

        # Botón de ejecución con efecto neon
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
        
        # Mensaje de bienvenida con estilo futurista
        self.display_welcome_message()
    
    def set_neon_theme(self):
        """Configura el tema neon futurista"""
        self.root.configure(bg='#0a0a12')
        
        # Configurar colores neon
        self.neon_blue = '#00fffc'
        self.neon_pink = '#ff00ff'
        self.neon_purple = '#6a00ff'
        self.dark_bg = '#0a0a12'
        self.darker_bg = '#050510'
        
        # Configurar estilos ttk
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
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
║  ███╗   ██╗███████╗ ██████╗ ███╗   ██╗███████╗       ║
║  ████╗  ██║██╔════╝██╔═══██╗████╗  ██║██╔════╝       ║
║  ██╔██╗ ██║█████╗  ██║   ██║██╔██╗ ██║███████╗       ║
║  ██║╚██╗██║██╔══╝  ██║   ██║██║╚██╗██║╚════██║       ║
║  ██║ ╚████║███████╗╚██████╔╝██║ ╚████║███████║       ║
║  ╚═╝  ╚═══╝╚══════╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝       ║
╠══════════════════════════════════════════════════════╣
║  TERMINAL NEON v2.0 - Escribe 'ayuda' para comenzar  ║
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