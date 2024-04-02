# pylint: disable=import-error, no-name-in-module
# Desativa os alertas de erro de importação pelo pylint.

from __future__ import print_function
# Importa a função print_function do módulo __future para garantir compatibilidade com a sintaxe de impressão do Python 3.

import os
import json
from ingresso_generator import overlay_code_on_image, generate_ingresso_code
from email_sender import send_email
from google_sheets import read_google_sheets, authorize_google_sheets
# from decouple import Config, Csv, RepositoryEnv
from dotenv import load_dotenv
from cloud_storage_functions import guardar_en_gcs, leer_desde_gcs

load_dotenv()

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
# Escopos OAuth 2.0 necessários para ler dados do Google Sheets.

# Cria uma instância do Config e configura o caminho para o arquivo .env
# config = Config(RepositoryEnv('../.env'))

# Lê as variáveis de ambiente do arquivo .env
SPREADSHEET_ID = os.getenv('SPREADSHEET_ID')
SHEET_NAME = os.getenv('SHEET_NAME')

# Configurações do servidor de e-mail
EMAIL_SMTP_SERVER = os.getenv('EMAIL_SMTP_SERVER')
EMAIL_SMTP_PORT = os.getenv('EMAIL_SMTP_PORT')
EMAIL_USERNAME = os.getenv('EMAIL_USERNAME')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')

# Dicionário padrão para armazenar os contadores.
DEFAULT_CONTADORES = {'SOCIAL': 0, 'INTEIRA': 0, 'MEIA': 0}

def read_last_processed_row(file_path):
    datos = leer_desde_gcs(file_path)
    if not datos:
        return 0
    return datos
    # Lê o número da última linha processada a partir do arquivo de configuração.
    #if os.path.exists(file_path):
    #    with open(file_path, 'r') as file:
    #        data = json.load(file)
    #        return data.get('last_processed_row', 0)
    #else:
    #    return 0

def update_last_processed_row(last_row, file_path):
    # Atualiza o número da última linha processada no arquivo de configuração.
    data = {'last_processed_row': last_row}
    guardar_en_gcs(data, file_path)
    
    #with open(file_path, 'w') as file:
    #    json.dump(data, file)

def read_contadores(file_path, default_contadores):
    # Lê os contadores a partir do arquivo ou utiliza o padrão se o arquivo não existir.
    datos = leer_desde_gcs(file_path)
    if not datos:
        return default_contadores
    return datos
    
    #if os.path.exists(file_path):
    #    with open(file_path, 'r') as file:
    #        data = json.load(file)
    #        return data
    #else:
    #    return default_contadores

def save_contadores(contadores, file_path):
    # Salva os contadores no arquivo.
    
    guardar_en_gcs(contadores, file_path)
    #with open(file_path, 'w') as file:
    #    json.dump(contadores, file)

def main():
    # Inicializa as credenciais e o serviço do Google Sheets.
    sheets_service = authorize_google_sheets()

    # Constrói a string de intervalo para obter valores das colunas B, C e E na planilha especificada.
    range_name = f'{SHEET_NAME}!B:E'

    # Lê o número da última linha processada a partir do arquivo de configuração.
    #last_processed_row_file = './data/last_processed_row.json'
    last_processed_row_file = 'gs://data_pdm/last_processed_row.json'
    last_processed_row = read_last_processed_row(last_processed_row_file)

    # Lê os contadores a partir do arquivo ou utiliza o padrão se o arquivo não existir.
    #contadores_file = './data/contadores.json'
    contadores_file = 'gs://data_pdm/contadores.json'
    contadores = read_contadores(contadores_file, DEFAULT_CONTADORES)

    # Lê os dados do Google Sheets.
    values = read_google_sheets(sheets_service, SPREADSHEET_ID, range_name)

    # Verifica se há novas linhas desde a última execução.
    if values and last_processed_row < len(values):
        # Calcula o índice da última linha e obtém seus valores, se existirem.
        last_row = len(values)
        last_row_values = values[last_processed_row:]

        # Atualiza o número da última linha processada.
        update_last_processed_row(last_row, last_processed_row_file)

        # Itera sobre as linhas intermediárias e executa o processamento.
        for row_values in last_row_values:
            if len(row_values) >= 4:
                if last_processed_row == 0:
                    continue

                coluna_b, coluna_c, coluna_e = row_values[0], row_values[1], row_values[3]

                print(f"Tipo de Ingresso: {coluna_e}")

                ingresso_code = generate_ingresso_code(coluna_e, contadores)
                image_path = overlay_code_on_image(ingresso_code)

                print(f"Código do Ingresso: {ingresso_code}")
                print(f"Índice da Linha: {last_row}")
                print(f"Valores da Linha: {row_values}\n")

                send_email(
                    to_email=coluna_b,
                    attachment_path=image_path,
                    nome_pessoa=coluna_c,
                    email_smtp_server=EMAIL_SMTP_SERVER,
                    email_smtp_port=EMAIL_SMTP_PORT,
                    email_username=EMAIL_USERNAME,
                    email_password=EMAIL_PASSWORD
                )

                save_contadores(contadores, contadores_file)
            else:
                print(f"Linha ignorada. Índice da Linha: {last_row}, Valores da Linha: {row_values}")
    else:
        print("Não há novos dados desde a última execução.")

if __name__ == '__main__':
    # Adicione essas linhas para debug
    SPREADSHEET_ID =  os.getenv('SPREADSHEET_ID')
    SHEET_NAME =  os.getenv('SHEET_NAME')
    
    print(f"SHEET_NAME: {SHEET_NAME}")

    main()
