#!/usr/bin/env python3
"""
Email Sender Module
Sends generated load test summary emails via SMTP
"""
 
import smtplib
import json
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
 
class EmailSender:
    def __init__(self, config_path="config/recipients.json"):
        load_dotenv("config/.env")
        self.smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", 587))
        self.sender_email = os.getenv("SENDER_EMAIL")
        self.sender_password = os.getenv("SENDER_PASSWORD")
        self.use_tls = os.getenv("SMTP_USE_TLS", "true").lower() == "true"
        with open(config_path, 'r') as f:
            self.config = json.load(f)
    def send_email(self, recipient_list, subject, body_html):
        """
        Send email to multiple recipients
        Args:
            recipient_list: List of email addresses
            subject: Email subject
            body_html: HTML formatted email body
        """
        try:
            # Create message
            message = MIMEMultipart("alternative")
            message["Subject"] = subject
            message["From"] = self.sender_email
            message["To"] = ", ".join(recipient_list)
            # Attach HTML content
            html_part = MIMEText(body_html, "html")
            message.attach(html_part)
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                if self.use_tls:
                    server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.sendmail(self.sender_email, recipient_list, message.as_string())
            print(f"✓ Email sent successfully to {len(recipient_list)} recipients")
            return True
        except Exception as e:
            print(f"✗ Error sending email: {str(e)}")
            return False
 
def main():
    sender = EmailSender()
    recipients = sender.config.get('recipients', [])
    subject = "Load Test Summary Report"
    # Read generated email
    with open("output/email_summary.html", 'r') as f:
        body = f.read()
    sender.send_email(recipients, subject, body)
 
if __name__ == "__main__":
    main()
