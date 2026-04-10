import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from imap_tools import MailBox, AND
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

class EmailReader:
    """
    Clase para leer correos electrónicos de una cuenta IMAP.
    Utiliza imap_tools para facilitar el acceso a los mensajes.
    """
    def __init__(self, server, user, password):
        self.server = server
        self.user = user
        self.password = password

    def fetch_emails(self, criteria=AND(all=True), limit=5):
        """
        Recupera una lista de correos que coincidan con el criterio dado.
        
        :param criteria: Filtro de búsqueda (por defecto todos los correos)
        :param limit: Número máximo de correos a recuperar
        :return: Lista de objetos de correo (MailMessage)
        """
        emails = []
        try:
            # Conexión al servidor IMAP
            with MailBox(self.server).login(self.user, self.password) as mailbox:
                # Buscar correos en la bandeja de entrada (INBOX)
                for msg in mailbox.fetch(criteria, limit=limit, reverse=True):
                    emails.append({
                        'id': msg.uid,
                        'subject': msg.subject,
                        'from': msg.from_,
                        'date': msg.date,
                        'text': msg.text,
                        'html': msg.html
                    })
            return emails
        except Exception as e:
            print(f"Error al leer correos: {e}")
            return []

class EmailSender:
    """
    Clase para enviar correos electrónicos mediante un servidor SMTP.
    """
    def __init__(self, server, port, user, password):
        self.server = server
        self.port = port
        self.user = user
        self.password = password

    def send_email(self, to_email, subject, body, is_html=False):
        """
        Envía un correo electrónico con la marca de agua de MFL4bs.
        
        :param to_email: Dirección de destino
        :param subject: Asunto del mensaje
        :param body: Contenido del mensaje (texto o HTML)
        :param is_html: Indica si el cuerpo del mensaje es HTML
        """
        try:
            # Agregar marca de agua de MFL4bs al final del mensaje
            watermark = "\n\n--- Enviado automáticamente por MFL4bs ---"
            if is_html:
                watermark = "<br><br><hr><p style='color: gray;'><i>Enviado automáticamente por <b>MFL4bs</b></i></p>"
            
            full_body = body + watermark

            # Crear el objeto del mensaje
            message = MIMEMultipart()
            message["From"] = self.user
            message["To"] = to_email
            message["Subject"] = subject

            # Adjuntar el cuerpo (texto plano o HTML)
            message.attach(MIMEText(full_body, "html" if is_html else "plain"))

            # Establecer conexión segura con el servidor SMTP
            with smtplib.SMTP(self.server, self.port) as server:
                server.starttls()  # Iniciar cifrado TLS para seguridad
                server.login(self.user, self.password)
                # Enviar el correo
                server.sendmail(self.user, to_email, message.as_string())
                print(f"Correo enviado exitosamente a {to_email}")
                return True
        except Exception as e:
            print(f"Error al enviar correo: {e}")
            return False

def main():
    # Obtener credenciales desde variables de entorno
    email_user = os.getenv("EMAIL_USER")
    email_pass = os.getenv("EMAIL_PASS")
    imap_server = os.getenv("IMAP_SERVER")
    smtp_server = os.getenv("SMTP_SERVER")
    smtp_port = int(os.getenv("SMTP_PORT", 587))

    if not all([email_user, email_pass, imap_server, smtp_server]):
        print("Error: Por favor configura las variables de entorno en el archivo .env")
        return

    # Instanciar el lector de correos
    reader = EmailReader(imap_server, email_user, email_pass)
    
    print("\n--- Leyendo últimos 3 correos ---")
    emails = reader.fetch_emails(limit=3)
    for i, mail in enumerate(emails, 1):
        print(f"{i}. De: {mail['from']} | Asunto: {mail['subject']}")
        # Aquí podrías agregar lógica para responder automáticamente basado en el contenido

    # Instanciar el remitente de correos
    sender = EmailSender(smtp_server, smtp_port, email_user, email_pass)
    
    # Ejemplo de envío automático (Comentado para evitar spam accidental)
    # response_subject = "Re: Confirmación de lectura automática"
    # response_body = "Hola, he recibido tu correo. Este es un mensaje automático de mi Email Reader en Python."
    # sender.send_email("destinatario@ejemplo.com", response_subject, response_body)

if __name__ == "__main__":
    main()
