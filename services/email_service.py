import smtplib

from email.mime.text import MIMEText

def enviar_email(
    nome,
    usuario,
    email
):

    try:

        remetente = "SEUEMAIL@gmail.com"

        senha_email = "SENHA_DO_EMAIL"

        mensagem = MIMEText(

            f"""

Olá {nome}!

Seu cadastro na SGO Motos foi realizado com sucesso.

Usuário: {usuario}

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

    except:

        print("Erro ao enviar email")