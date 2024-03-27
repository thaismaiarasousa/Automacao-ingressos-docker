import json
import os

class Model:
    def __init__(self, file_path, default_values):
        self.file_path = file_path
        self.data = self.load_data(default_values)

    def load_data(self, default_values):
        # Carrega os dados do arquivo ou usa valores padrão se o arquivo não existir.
        if not self.file_path:
            return default_values

        if not os.path.exists(self.file_path):
            return default_values

        with open(self.file_path, 'r') as file:
            data = json.load(file)
            return data

    def save_data(self):
        # Salva os dados no arquivo, se o caminho do arquivo estiver especificado.
        if self.file_path:
            with open(self.file_path, 'w') as file:
                json.dump(self.data, file)
