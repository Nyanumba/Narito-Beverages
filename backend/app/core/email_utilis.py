import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.core.config import settings 

def send_verification_email(to_email: str, token: str):
    verify_link = f"http://127.0.0.1:8000/auth/verify-email?token={token}"

    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Verify your Narito Beverages account"
    msg["From"] = settings.mail_from
    msg["To"] = to_email

    html = f"""
    <html>
      <body>
        <h2>Welcome to Narito Beverages!</h2>
        <p>Click below to verify your email address:</p>
        <a href="{verify_link}">Verify Email</a>
      </body>
    </html>
    """

    msg.attach(MIMEText(html, "html"))

    try:
        with smtplib.SMTP(settings.mail_server, settings.mail_port) as server:
            server.starttls()
            server.login(settings.mail_username, settings.mail_password)
            server.sendmail(settings.mail_from, to_email, msg.as_string())
            print("✅ Verification email sent successfully.")
    except Exception as e:
        print(f"❌ Error sending email: {e}")