# Automacao-Ingressos

Este projeto é uma automação para processar dados de um Google Sheets, gerar ingresso com códigos únicos e enviá-los por e-mail;
contando, também, com contadores para cada tipo de ingresso (o que favorece a gestão das vendas dos mesmos). É útil para gestão de eventos que exigem emissão de ingressos personalizados.

## Funcionalidades

- **Leitura de Dados:** Lê dados de uma planilha do Google Sheets, alimentada por um Formulário Google.
- **Geração de Códigos:** Gera códigos de ingresso com base nas informações da planilha.
- **Processamento de imagem:** Subescrição do código único em imagem padrão.
- **Envio por E-mail:** Envia os ingresso personalizados por e-mail com anexo.

## Configuração

1. Configure suas variáveis de ambiente no arquivo `.env`.
2. Instale as dependências: `pip install -r requirements.txt`.
3. Integre e configure sua API Google Sheets em Google Cloud Console.

## Uso

Execute o script principal:
python main.py



