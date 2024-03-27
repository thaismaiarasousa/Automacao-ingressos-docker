import os
from PIL import Image, ImageDraw, ImageFont

def generate_ingresso_code(tipo_ingresso, contadores):
    # Lógica para gerar o código do ingresso com base no tipo.
    # Por exemplo, você pode usar um contador para cada tipo de ingresso.
    # Suponha que você tenha um dicionário para armazenar o contador de cada tipo.
    # Cada vez que encontrar um novo ingresso do mesmo tipo, incrementa o contador.
    # O código gerado seria composto pelo tipo de ingresso + número do contador.

    # Obtém o tipo de ingresso atual e converte para maiúsculas.
    tipo_ingresso = tipo_ingresso.upper()

    # Incrementa o contador correspondente ao tipo de ingresso.
    if "SOCIAL" in tipo_ingresso:
        contadores['SOCIAL'] += 1
        contador = contadores['SOCIAL']
        # Gera o código do ingresso.
        ingresso_code = f"SOCIAL{contador:02}"
    elif "INTEIRA" in tipo_ingresso:
        contadores['INTEIRA'] += 1
        contador = contadores['INTEIRA']
        # Gera o código do ingresso.
        ingresso_code = f"INTEIRA{contador:02}"
    else:
        contadores['MEIA'] += 1
        contador = contadores['MEIA']
        # Gera o código do ingresso.
        ingresso_code = f"MEIA{contador:02}"

    return ingresso_code

def overlay_code_on_image(ingresso_code):
    # Lógica para sobrepor o código gerado na imagem padrão.
    # Carrega a imagem padrão (substitua 'caminho_da_imagem_padrao' pelo caminho real).
    base_image = Image.open('./images/ingresso_padrao/ingresso_padrao.jpg')

    # Cria um objeto ImageDraw para desenhar na imagem.
    draw = ImageDraw.Draw(base_image)

    # Escolhe a fonte (substitua 'caminho_da_fonte' pela fonte real).
    font_size = 35  # Tamanho da fonte (ajuste conforme necessário)
    font = ImageFont.truetype("arial.ttf", font_size)

    # Escolhe a posição onde o código será sobreposto (ajuste conforme necessário).
    position = (130, 50)

    # Escolhe a cor do texto.
    text_color = (250, 250, 250)  # Preto

    # Sobrepoõe o texto (código do ingresso) na imagem.
    draw.text(position, ingresso_code, font=font, fill=text_color)

    # Escolhe o diretório onde deseja salvar a imagem resultante.
    output_directory = './images/ingressos_editados'

    # Garante que o diretório existe; se não existir, cria.
    os.makedirs(output_directory, exist_ok=True)

    # Salva ou mostra a imagem resultante no diretório especificado.
    output_path = os.path.join(output_directory, f'seu_ingresso{ingresso_code}.png')
    base_image.save(output_path)

    return output_path