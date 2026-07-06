import os
import smtplib

from email.mime.text import MIMEText
from dotenv import load_dotenv

# Carrega variáveis do .env
load_dotenv()


# =========================
# CONFIGURAÇÃO SMTP
# =========================
EMAIL = os.getenv("EMAIL")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")


def enviar_email_cadastro(nome, usuario, email):
    try:
        mensagem = MIMEText(f"""
Olá {nome}!

Seu cadastro na SGO Motos foi realizado com sucesso.

Usuário: {usuario}

Obrigado por utilizar nosso sistema!
""")

        mensagem["Subject"] = "Cadastro realizado"
        mensagem["From"] = EMAIL
        mensagem["To"] = email

        servidor = smtplib.SMTP("smtp.gmail.com", 587)
        servidor.starttls()
        servidor.login(EMAIL, EMAIL_PASSWORD)
        servidor.send_message(mensagem)
        servidor.quit()

        print("E-mail de cadastro enviado com sucesso!")

    except Exception as erro:
        print("Erro ao enviar e-mail de cadastro:", erro)


# =========================
# RECUPERAÇÃO DE SENHA
# =========================
def enviar_email_recuperacao(email, token):
    try:
        link = f"https://sgo-motos.onrender.com/redefinir-senha/{token}"

        mensagem = MIMEText(f"""
Olá!

Recebemos uma solicitação para redefinir sua senha.

Clique no link abaixo para criar uma nova senha:

{link}

Este link é válido por 30 minutos.

Se você não solicitou isso, ignore este e-mail.
""")

        mensagem["Subject"] = "Recuperação de senha"
        mensagem["From"] = EMAIL
        mensagem["To"] = email

        servidor = smtplib.SMTP("smtp.gmail.com", 587)
        servidor.starttls()
        servidor.login(EMAIL, EMAIL_PASSWORD)
        servidor.send_message(mensagem)
        servidor.quit()

        print("E-mail de recuperação enviado com sucesso!")

    except Exception as erro:
        print("Erro ao enviar e-mail de recuperação:", erro)