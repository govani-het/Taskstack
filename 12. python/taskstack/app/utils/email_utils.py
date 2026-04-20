"""Email utility functions."""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os


async def send_password_reset_email(to_email: str, token: str) -> None:
    """Send password reset email with token.

    Args:
        to_email: Recipient email address.
        token: Password reset token.
    """
    smtp_server = os.getenv("SMTP_SERVER")
    smtp_port = int(os.getenv("SMTP_PORT", 587))
    smtp_username = os.getenv("SMTP_USERNAME")
    smtp_password = os.getenv("SMTP_PASSWORD")

    if not all([smtp_server, smtp_username, smtp_password]):
        raise ValueError("SMTP configuration is incomplete")

    # Create message
    msg = MIMEMultipart()
    msg['From'] = smtp_username
    msg['To'] = to_email
    msg['Subject'] = "Password Reset Request"

    # Email body
    body = f"""
    You have requested to reset your password.

    Your password reset token is: {token}

    This token will expire in 15 minutes.

    If you did not request this, please ignore this email.
    """
    msg.attach(MIMEText(body, 'plain'))

    # Send email
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        text = msg.as_string()
        server.sendmail(smtp_username, to_email, text)
        server.quit()
    except Exception as e:
        # In production, you might want to log this
        raise e