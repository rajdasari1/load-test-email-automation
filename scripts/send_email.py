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
        self.smtp_server = os.getenv("SMTP_SERVER", "rajdasari@deloitte.com")
        # Handle empty SMTP_PORT
        smtp_port_str = os.getenv("SMTP_PORT", "587")
        try:
            self.smtp_port = int(smtp_port_str) if smtp_port_str else 587
        except ValueError:
            print(f"Warning: Invalid SMTP_PORT '{smtp_port_str}', using default 587")
            self.smtp_port = 587
        self.sender_email = os.getenv("SENDER_EMAIL")
        self.sender_password = os.getenv("SENDER_PASSWORD")
        self.use_tls = os.getenv("SMTP_USE_TLS", "true").lower() == "true"
        # Validate credentials
        if not self.sender_email or not self.sender_password:
            print("⚠️  Warning: Email credentials not configured. Skipping email send.")
            print(f"   SENDER_EMAIL: {'✓ Set' if self.sender_email else '✗ Not set'}")
            print(f"   SENDER_PASSWORD: {'✓ Set' if self.sender_password else '✗ Not set'}")
            return
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
        # Check if credentials are set
        if not self.sender_email or not self.sender_password:
            print("⚠️  Skipping email send: credentials not configured")
            print("   Please set SENDER_EMAIL and SENDER_PASSWORD in GitHub Secrets")
            return False
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
    if not os.path.exists("output/email_summary.html"):
        print("Error: output/email_summary.html not found")
        return
    with open("output/email_summary.html", 'r') as f:
        body = f.read()
    sender.send_email(recipients, subject, body)
 
if __name__ == "__main__":
    main()
