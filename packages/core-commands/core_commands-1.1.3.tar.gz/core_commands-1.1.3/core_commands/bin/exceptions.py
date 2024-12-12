class UnknownCommand(Exception):
    def __init__(self, message):
        self.message = f"Comando desconocido: {message}"
        super().__init__(self.message)