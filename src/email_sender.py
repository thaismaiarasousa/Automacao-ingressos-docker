import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def send_email(to_email, attachment_path, nome_pessoa, email_smtp_server, email_smtp_port, email_username, email_password):
    # Configuração inicial do servidor SMTP
    smtp_server = smtplib.SMTP(email_smtp_server, email_smtp_port)
    smtp_server.starttls()

    # Autenticação no servidor SMTP
    smtp_server.login(email_username, email_password)

    # Construção do e-mail
    sender_email = email_username
    receiver_email = to_email
    subject = "Ticket CABARET BURLESQUE - Cia. Pé de Manga"
    
    # Personaliza a mensagem do corpo do e-mail com o nome da pessoa
    body = f"Olá, {nome_pessoa}! Tudo bem? ☀️✨\nSeguem, em anexo, os ticket referente ao nosso espetáculo “CABARET BURLESQUE”, que acontecerá no sábado 20 de Julho, pontualmente às 19h. \nQualquer dúvida estamos por aqui e no instagram @ciapedemanga. \nAté lá! \nThai,  \nCia. Pé de Manga"

    # Criar mensagem MIMEMultipart
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject

    # Adicionar corpo ao e-mail
    message.attach(MIMEText(body, "plain"))

    # Adicionar anexo ao e-mail
    with open(attachment_path, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f"attachment; filename= {os.path.basename(attachment_path)}")
        message.attach(part)

    # Enviar e-mail
    smtp_server.sendmail(sender_email, receiver_email, message.as_string())

    # Finalizar a conexão SMTP
    smtp_server.quit()
