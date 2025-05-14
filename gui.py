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

        #Mostrar la terminal
        self.output_frame = tk.Frame(self.root)
        self.output_frame.pack(fill=tk.BOTH, expand=True)

        #Frame interno que contiene el texto y el scrollbar
        self.text_container = tk.Frame(self.output_frame)
        self.text_container.pack(fill=tk.BOTH, expand=True)

        # crollbar
        scrollbar = tk.Scrollbar(self.text_container)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        #Widget de salida
        self.text_output = tk.Text(self.text_container, wrap=tk.WORD, height=15, yscrollcommand=scrollbar.set)
        self.text_output.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar.config(command=self.text_output.yview)


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

        #Eventos de botón
        self.command_entry.bind("<Return>", self.execute_command)
        self.command_entry.bind("<Up>", self.show_previous_command)
        self.command_entry.bind("<Down>", self.show_next_command)

        #Historial de comandos
        self.command_history = []
        self.history_index = -1


    def execute_command(self, event=None):
        self.text_output.config(state="normal")
        command = self.command_entry.get()
        self.command_history.append(command)
        self.history_index = len(self.command_history)
        self.shell.execute(command)
        self.text_output.see("end")
        self.text_output.config(state="disabled")
        self.command_entry.delete(0, tk.END)

    def show_previous_command(self, event = None):
        if self.command_history and self.history_index > 0:
            self.history_index -= 1
            self.command_entry.delete(0, tk.END)
            self.command_entry.insert(0, self.command_history[self.history_index])
        return "break"

    def show_next_command(self, event = None):
        if self.command_history and self.history_index < len(self.command_history) - 1:
            self.history_index += 1
            self.command_entry.delete(0, tk.END)
            self.command_entry.insert(0, self.command_history[self.history_index])
        else:
            self.history_index = len(self.command_history)
            self.command_entry.delete(0, tk.END)
        return "break"