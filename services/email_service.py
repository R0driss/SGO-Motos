import os
import smtplib

from email.mime.text import MIMEText


def enviar_email(
    nome,
    usuario,
    email
):

    try:

        remetente = os.getenv("EMAIL")

        senha_email = os.getenv("EMAIL_PASSWORD")

        mensagem = MIMEText(
            f"""
Olá {nome}!

Seu cadastro na SGO Motos foi realizado com sucesso.

Usuário: {usuario}

Obrigado por utilizar nosso sistema!
"""
        )

        mensagem["Subject"] = "Cadastro realizado"

        mensagem["From"] = remetente

        mensagem["To"] = email

        servidor = smtplib.SMTP(
            "smtp.gmail.com",
            587
        )

        servidor.starttls()

        servidor.login(
            remetente,
            senha_email
        )

        servidor.send_message(mensagem)

        servidor.quit()

    except Exception as erro:

        print("Erro ao enviar e-mail:", erro)


def enviar_email_recuperacao(
    email,
    token
):

    try:

        remetente = os.getenv("EMAIL")

        senha_email = os.getenv("EMAIL_PASSWORD")

        link = (
            f"https://sgo-motos.onrender.com/redefinir-senha/{token}"
        )

        mensagem = MIMEText(
            f"""
Olá!

Recebemos uma solicitação para redefinir sua senha.

Clique no link abaixo para criar uma nova senha:

{link}

Este link é válido por 30 minutos.

Se você não solicitou esta alteração, ignore este e-mail.
"""
        )

        mensagem["Subject"] = "Recuperação de senha"

        mensagem["From"] = remetente

        mensagem["To"] = email

        servidor = smtplib.SMTP(
            "smtp.gmail.com",
            587
        )

        servidor.starttls()

        servidor.login(
            remetente,
            senha_email
        )

        servidor.send_message(mensagem)

        servidor.quit()

    except Exception as erro:

        print("Erro ao enviar e-mail:", erro)