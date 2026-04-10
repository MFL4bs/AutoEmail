import unittest
from unittest.mock import MagicMock, patch
from email_manager import EmailReader, EmailSender
import email

class TestEmailManager(unittest.TestCase):
    """
    Pruebas unitarias para las clases EmailReader y EmailSender.
    Utiliza mocks para simular las conexiones de red y servidores.
    """

    def setUp(self):
        # Credenciales de prueba (falsas)
        self.user = "test@example.com"
        self.password = "password123"
        self.imap_server = "imap.example.com"
        self.smtp_server = "smtp.example.com"
        self.smtp_port = 587

    @patch('email_manager.MailBox')
    def test_fetch_emails(self, mock_mailbox):
        """Prueba que EmailReader.fetch_emails funciona correctamente con mocks."""
        # Configurar el mock para imap_tools
        mock_msg = MagicMock()
        mock_msg.uid = "123"
        mock_msg.subject = "Prueba de asunto"
        mock_msg.from_ = "remitente@test.com"
        mock_msg.date = "2024-01-01"
        mock_msg.text = "Cuerpo del mensaje"
        mock_msg.html = "<html><body>Cuerpo del mensaje</body></html>"

        # Simular el comportamiento del MailBox (context manager y fetch)
        mock_instance = mock_mailbox.return_value
        mock_instance.login.return_value.__enter__.return_value.fetch.return_value = [mock_msg]

        reader = EmailReader(self.imap_server, self.user, self.password)
        emails = reader.fetch_emails(limit=1)

        # Verificaciones
        self.assertEqual(len(emails), 1)
        self.assertEqual(emails[0]['subject'], "Prueba de asunto")
        self.assertEqual(emails[0]['from'], "remitente@test.com")

    @patch('email_manager.smtplib.SMTP')
    def test_send_email(self, mock_smtp):
        """Prueba que EmailSender.send_email funciona correctamente con mocks."""
        # Simular el comportamiento del servidor SMTP (context manager)
        mock_instance = mock_smtp.return_value.__enter__.return_value

        sender = EmailSender(self.smtp_server, self.smtp_port, self.user, self.password)
        body_test = "Hola mundo"
        success = sender.send_email("destinatario@test.com", "Asunto de prueba", body_test)

        # Verificaciones
        self.assertTrue(success)
        # Verificar que se llamó a starttls y login
        mock_instance.starttls.assert_called_once()
        mock_instance.login.assert_called_with(self.user, self.password)
        # Verificar que se llamó a sendmail y que el cuerpo contiene la marca de agua
        args, kwargs = mock_instance.sendmail.call_args
        sent_message_str = args[2]
        
        # Parsear el mensaje para leer el contenido decodificado
        msg = email.message_from_string(sent_message_str)
        found_watermark = False
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                payload = part.get_payload(decode=True).decode()
                if "MFL4bs" in payload:
                    found_watermark = True
                    break
        
        self.assertTrue(found_watermark, "No se encontró la marca de agua 'MFL4bs' en el cuerpo del correo")

if __name__ == "__main__":
    unittest.main()
