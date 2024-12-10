import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configurações do servidor e login
MAIL_FROM = os.environ.get("MAIL_FROM", "")
MAIL_TO = os.environ.get("MAIL_TO", "")
MAIL_SMTP_SERVER = os.environ.get("MAIL_SMTP_SERVER", "")
MAIL_SMTP_PORT = int(os.environ.get("MAIL_SMTP_PORT", "0"))
MAIL_USER = os.environ.get("MAIL_USER", "")
MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD", "")
MAIL_USE_SSL = not os.environ.get("MAIL_USE_SSL") is None

class MailNotification:
    """ Classe responsável pela notificação via e-mail """

    def send_mail(subject : str, body : str):
        """ Enviar um e-mail """
        # Conectar ao servidor SMTP e enviar o e-mail
        try:

            # Conectando ao servidor SMTP (Gmail)
            server = smtplib.SMTP(MAIL_SMTP_SERVER, MAIL_SMTP_PORT)

            try:

                if MAIL_USE_SSL:
                    server.starttls()  # Usar TLS para segurança

                server.login(MAIL_USER, MAIL_PASSWORD)  # Login no servidor SMTP

                # Criar o cabeçalho do e-mail
                msg = MIMEMultipart()
                msg["From"] = MAIL_FROM
                msg["To"] = MAIL_TO
                msg["Subject"] = subject
                msg.attach(MIMEText(body, "plain"))

                # Enviar o e-mail
                text_message = msg.as_string()
                server.sendmail(MAIL_FROM, MAIL_TO, text_message)
                
            finally:
                server.quit()  # Encerrar a conexão com o servidor

        except Exception as e:
            raise e
