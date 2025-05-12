"""En este modulo se define la interfaz gráfica de la app. 
solo se encarga de la parte visual y de la interacción con el usuario."""
import tkinter as tk
from shell import Shell
from commands import Commands
from utils import get_current_path

class CustomShellUI:
    def __init__(self, root):
        self.root = root
        self.root.title("SisShell")
        self.root.geometry("600x400")

        #Objeto shell y comandos
        self.shell = Shell(self)
        self.commands = Commands(self.shell)

        #mostrar la terminal
        self.output_frame = tk.Frame(self.root)
        self.output_frame.pack(fill = tk.BOTH, expand = True)

        #Widget para mostrar los resultados de los comandos
        self.text_output = tk.Text(self.output_frame, wrap = tk.WORD, height = 15)
        self.text_output.pack(fill = tk.BOTH, expand = True)

        #Entrada de los comandos
        self.input_frame = tk.Frame(self.root)
        self.input_frame.pack(fill=tk.X)

        self.command_entry = tk.Entry(self.input_frame, width=50)
        self.command_entry.pack(side=tk.LEFT, padx=5, pady=5)
        self.command_entry.bind("<Return>", self.execute_command)

        # Barra de ruta
        self.current_path = get_current_path()
        self.path_label = tk.Label(self.root, text=self.current_path, anchor="w")
        self.path_label.pack(fill=tk.X)

    def execute_command(self, event=None):
        command = self.command_entry.get()
        self.shell.execute(command)
        self.command_entry.delete(0, tk.END)