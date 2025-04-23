import smtplib

from app.core.config import settings


def send_email(to_email, first_name, url):
    smtp_server = settings.SMTP_SERVER
    port = settings.SMTP_PORT
    email = settings.SUPER_EMAIL
    password = settings.SUPER_EMAIL_PASSWORD
    subject = settings.COMPANY_NAME
    message = f"""Email Verification
            Dear { first_name },
            Thank you for registering on our platform. Please click the button below to verify your email address:       
            { url }
            """
    try:
        with smtplib.SMTP(smtp_server, port) as server:
            server.starttls()
            server.login(email, password)
            server.sendmail(email, to_email, f'Subject: {subject}\n\n{message}')
    except smtplib.SMTPException as e:
        raise
