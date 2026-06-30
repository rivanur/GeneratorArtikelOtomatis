import os
import requests
import logging

logger = logging.getLogger(__name__)

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_verification_email(to_email: str, token: str, request_url_base: str):
    """
    Kirim email verifikasi menggunakan Webhook Google Apps Script
    """
    script_url = os.getenv("GOOGLE_SCRIPT_URL")
    
    if not script_url:
        logger.warning("GOOGLE_SCRIPT_URL belum diatur di .env. Pengiriman email dilewati.")
        return False
    
    verification_link = f"{request_url_base}/api/auth/verify?token={token}"
    
    html_content = f"""
    <html>
    <body>
        <h2>Selamat datang di ARSA!</h2>
        <p>Terima kasih telah mendaftar. Untuk mulai membuat artikel otomatis, silakan verifikasi email Anda dengan mengklik tautan di bawah ini:</p>
        <p><a href="{verification_link}" style="display:inline-block;padding:10px 20px;background-color:#4F46E5;color:white;text-decoration:none;border-radius:5px;">Verifikasi Email Saya</a></p>
        <p style="color:#666;font-size:12px;margin-top:20px;"><em>* Tautan verifikasi ini akan kedaluwarsa dalam waktu 15 menit.</em></p>
        <br>
        <p>Salam,</p>
        <p>Tim ARSA</p>
    </body>
    </html>
    """
    
    payload = {
        "to": to_email,
        "subject": "Verifikasi Email Pendaftaran ARSA",
        "htmlBody": html_content
    }
    
    try:
        response = requests.post(script_url, json=payload)
        
        if response.status_code == 200:
            logger.info(f"Email verifikasi berhasil dikirim ke {to_email} via Webhook")
            return True
        else:
            logger.error(f"Gagal mengirim email ke {to_email}. Status code: {response.status_code}")
            return False
            
    except Exception as e:
        logger.error(f"Error saat mengirim email via Webhook ke {to_email}: {str(e)}")
        return False

