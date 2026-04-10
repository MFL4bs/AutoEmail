Este sistema automatizado permite interactuar con cuentas de correo electrónico utilizando protocolos estándar (IMAP para leer y SMTP para enviar). Está diseñado para ser seguro, modular y fácil de extender para tareas de automatización más complejas.

**Requisitos Previos**
- **Python 3.x** instalado.
- Una cuenta de correo (Gmail, Outlook, etc.).
- **Contraseña de Aplicación**: Si usas Gmail o servicios con 2FA, debes generar una contraseña específica para aplicaciones desde la configuración de seguridad de tu cuenta.

**Guía de Uso Paso a Paso**

**1. Instalación de Dependencias**
Primero, debes instalar las librerías necesarias ejecutando el siguiente comando en tu terminal:
```bash
python -m pip install -r requirements.txt
```
Esto instalará `imap-tools` para la lectura simplificada y `python-dotenv` para la gestión de credenciales.

**2. Configuración de Credenciales**
El sistema utiliza un archivo de entorno para mantener tus datos seguros:
- Localiza el archivo [.env.example](file:///c:/XCode/Email%20Reader/.env.example).
- Renómbralo a `.env`.
- Edita los valores con tu información real:
  - `EMAIL_USER`: Tu dirección de correo completa.
  - `EMAIL_PASS`: Tu contraseña de aplicación (no la normal de acceso).
  - `IMAP_SERVER`: Servidor de entrada (ej. `imap.gmail.com`).
  - `SMTP_SERVER`: Servidor de salida (ej. `smtp.gmail.com`).

**3. Ejecución del Sistema**
Para iniciar el lector y ver los últimos correos, ejecuta:
```bash
python email_manager.py
```
El script realizará lo siguiente:
- Conectará al servidor IMAP y mostrará los últimos 3 correos en la consola.
- Si descomentas las líneas de envío en la función `main()`, enviará un correo de prueba con la marca de agua automática de **MFL4bs**.

**4. Verificación de Funcionamiento**
Si deseas asegurarte de que la lógica de envío y lectura es correcta sin gastar datos o enviar correos reales, puedes ejecutar las pruebas unitarias:
```bash
python test_email_manager.py
```
Estas pruebas simulan los servidores y verifican que la marca de agua de **MFL4bs** se esté insertando correctamente en el cuerpo de los mensajes.

**Estructura del Código**
- **[email_manager.py](file:///c:/XCode/Email%20Reader/email_manager.py)**: El núcleo del programa.
  - `EmailReader`: Clase encargada de conectarse y extraer mensajes.
  - `EmailSender`: Clase encargada de componer y enviar mensajes con la firma automática.
- **Marca de Agua**: Cada vez que envíes un correo, el sistema añade automáticamente:
  - *En texto:* `--- Enviado automáticamente por MFL4bs ---`
  - *En HTML:* Una línea divisoria y la firma en cursiva y negrita.
