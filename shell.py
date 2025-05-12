"""Este modulo contiene la logica principal del shell.
Ejecuta los comandos ya esan personalizados o externos."""
from commands import Commands

class Shell:
    def __init__(self, ui):
        self.ui = ui
        self.commands = Commands(self)

    def execute(self, command_text):
        command_text = command_text.strip()
        if not command_text:
            return

        parts = command_text.split()
        command = parts[0].lower()
        args = parts[1:]  # argumentos del comando

        if command in self.commands.commands_dict:
            try:
                self.commands.commands_dict[command](*args)
            except Exception as e:
                self.ui.text_output.insert("end", f"Error ejecutando '{command}': {e}\n")
        else:
            self.commands.execute_external_command(command_text)