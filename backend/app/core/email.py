from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import logging
import smtplib
from app.core.configuracion import configuracion

logger = logging.getLogger(__name__)


def enviarEmail(emailA: str, asunto: str, contenidoHtml: str) -> bool:
    """
    Envía un correo electrónico usando SMTP configurado en .env.
    Si no hay servidor SMTP configurado (desarrollo local), imprime el mensaje en consola.
    """
    if not configuracion.smtpHost or not configuracion.smtpUser:
        logger.info(f"[EMAIL MOCK - MODO DESARROLLO] Para: {emailA} | Asunto: {asunto}")
        print("\n" + "=" * 60)
        print(f"📧 [EMAIL MOCK] Para: {emailA}")
        print(f"📌 Asunto: {asunto}")
        print("-" * 60)
        print(contenidoHtml)
        print("=" * 60 + "\n")
        return True

    try:
        mensaje = MIMEMultipart("alternative")
        mensaje["Subject"] = asunto
        mensaje["From"] = f"{configuracion.emailsFromName} <{configuracion.emailsFromEmail}>"
        mensaje["To"] = emailA

        parteHtml = MIMEText(contenidoHtml, "html", "utf-8")
        mensaje.attach(parteHtml)

        with smtplib.SMTP(configuracion.smtpHost, configuracion.smtpPort) as servidor:
            servidor.starttls()
            if configuracion.smtpPassword:
                servidor.login(configuracion.smtpUser, configuracion.smtpPassword)
            servidor.sendmail(configuracion.emailsFromEmail, [emailA], mensaje.as_string())

        logger.info(f"Email enviado exitosamente a {emailA}")
        return True
    except Exception as e:
        logger.error(f"Error al enviar email a {emailA}: {str(e)}")
        return False


def enviarEmailRecuperacionPassword(emailA: str, token: str) -> bool:
    """
    Envía la plantilla de correo con el enlace para restablecer la contraseña.
    """
    enlaceRestablecimiento = f"{configuracion.frontendUrl}/restablecer-password?token={token}"
    asunto = f"Restablecer contraseña - {configuracion.proyectoNombre}"

    contenidoHtml = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body {{ font-family: 'Segoe UI', Arial, sans-serif; background-color: #f4f6f9; margin: 0; padding: 20px; }}
            .card {{ max-width: 500px; margin: 0 auto; background: #ffffff; border-radius: 8px; padding: 30px; box-shadow: 0 4px 12px rgba(0,0,0,0.08); }}
            .btn {{ display: inline-block; padding: 12px 24px; background-color: #3b82f6; color: #ffffff; text-decoration: none; border-radius: 6px; font-weight: bold; margin-top: 20px; }}
            .footer {{ margin-top: 30px; font-size: 12px; color: #6b7280; text-align: center; }}
        </style>
    </head>
    <body>
        <div class="card">
            <h2>Recuperación de Contraseña</h2>
            <p>Has solicitado restablecer tu contraseña para acceder a <strong>{configuracion.proyectoNombre}</strong>.</p>
            <p>Haz clic en el siguiente botón para continuar. Este enlace expira en {configuracion.emailResetTokenExpireHours} horas:</p>
            <a href="{enlaceRestablecimiento}" class="btn" target="_blank">Restablecer Contraseña</a>
            <p style="margin-top: 25px; font-size: 13px; color: #6b7280;">
                Si el botón no funciona, copia y pega el siguiente enlace en tu navegador:<br>
                <a href="{enlaceRestablecimiento}">{enlaceRestablecimiento}</a>
            </p>
            <div class="footer">
                <p>Si no solicitaste este cambio, puedes ignorar este correo de forma segura.</p>
            </div>
        </div>
    </body>
    </html>
    """

    return enviarEmail(emailA, asunto, contenidoHtml)
