FROM python:3.11-slim-buster

RUN mkdir /app

COPY ./requirements.txt /app

RUN pip install --no-cache-dir -r /app/requirements.txt

RUN mkdir /app/src

COPY ./src /app/src 

RUN mkdir /app/images

COPY ./images /app/images

RUN mkdir /app/data

COPY ./data /app/data

COPY ./service_account.json /app/service_account.json

# Configurações de acesso ao Sheets
#ENV SENHA_DO_EMAIL=""
#ENV CLIENT_ID=""
#ENV CLIENT_SECRET=""
#ENV REFRESH_TOKEN=""
#ENV SPREADSHEET_ID=""
#ENV SHEET_NAME=""
#ENV CLIENT_SECRET_FILE=""

# Configurações servidor gmail
#ENV EMAIL_SMTP_SERVER=""
#ENV EMAIL_SMTP_PORT=
#ENV EMAIL_USERNAME=""
#ENV EMAIL_PASSWORD=""

WORKDIR /app

CMD ["python","./src/main.py"]