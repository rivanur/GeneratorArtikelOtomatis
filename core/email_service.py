import os
import requests
import logging

logger = logging.getLogger(__name__)

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_verification_email(to_email: str, token: str, request_url_base: str):
    """
    Kirim email verifikasi menggunakan Gmail SMTP
    """
    sender_email = os.getenv("SMTP_EMAIL", "")
    sender_password = os.getenv("SMTP_PASSWORD", "")
    
    if not sender_email or not sender_password:
        logger.warning(f"Kredensial SMTP tidak dikonfigurasi. Email verifikasi ke {to_email} dilewati.")
        return False
        
    verification_link = f"{request_url_base}/api/auth/verify?token={token}"
    
    # Setup pesan email (MIME)
    msg = MIMEMultipart("alternative")
    msg['Subject'] = "Verifikasi Email Pendaftaran ARSA"
    msg['From'] = f"Tim ARSA <{sender_email}>"
    msg['To'] = to_email
    
    html_content = f"""
    <html>
    <body>
        <h2>Selamat datang di ARSA!</h2>
        <p>Terima kasih telah mendaftar. Untuk mulai membuat artikel otomatis, silakan verifikasi email Anda dengan mengklik tautan di bawah ini:</p>
        <p><a href="{verification_link}" style="display:inline-block;padding:10px 20px;background-color:#4F46E5;color:white;text-decoration:none;border-radius:5px;">Verifikasi Email Saya</a></p>
        <br>
        <p>Salam,</p>
        <p>Tim ARSA</p>
    </body>
    </html>
    """
    
    msg.attach(MIMEText(html_content, 'html'))
    
    try:
        # Koneksi ke server Gmail SMTP
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  # Mengamankan koneksi
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        
        logger.info(f"Email verifikasi berhasil dikirim ke {to_email}")
        return True
    except Exception as e:
        logger.error(f"Error saat mengirim email ke {to_email}: {str(e)}")
        return False

