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
        self.smtp_server = os.getenv("SMTP_SERVER", "smtp.office365.com")
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
        # Load config - ALWAYS initialize this
        self.config = self.load_recipients_config(config_path)
        # Validate credentials
        if not self.sender_email or not self.sender_password:
            print("⚠️  WARNING: Email credentials not configured")
            print(f"   SENDER_EMAIL: {'✓ Set' if self.sender_email else '✗ Not set'}")
            print(f"   SENDER_PASSWORD: {'✓ Set' if self.sender_password else '✗ Not set'}")
    def load_recipients_config(self, config_path):
        """Load recipients configuration"""
        try:
            if os.path.exists(config_path):
                with open(config_path, 'r') as f:
                    return json.load(f)
            else:
                print(f"⚠️  Config file not found: {config_path}")
                return {'recipients': []}
        except Exception as e:
            print(f"✗ Error loading config: {str(e)}")
            return {'recipients': []}
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
            print("⚠️  Skipping email send: email credentials not configured")
            print("   Please set SENDER_EMAIL and SENDER_PASSWORD in GitHub Secrets")
            return False
        if not recipient_list:
            print("⚠️  Skipping email send: no recipients configured")
            return False
        try:
            print(f"📧 Sending email to {len(recipient_list)} recipient(s)...")
            # Create message
            message = MIMEMultipart("alternative")
            message["Subject"] = subject
            message["From"] = self.sender_email
            message["To"] = ", ".join(recipient_list)
            # Attach HTML content
            html_part = MIMEText(body_html, "html")
            message.attach(html_part)
            # Send email
            print(f"🔗 Connecting to {self.smtp_server}:{self.smtp_port}...")
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                if self.use_tls:
                    print("🔐 Starting TLS encryption...")
                    server.starttls()
                print("🔑 Authenticating...")
                server.login(self.sender_email, self.sender_password)
                print("📤 Sending message...")
                server.sendmail(self.sender_email, recipient_list, message.as_string())
            print(f"✓ Email sent successfully to {len(recipient_list)} recipient(s)")
            for recipient in recipient_list:
                print(f"  ✓ {recipient}")
            return True
        except smtplib.SMTPAuthenticationError as e:
            print(f"✗ Authentication failed: {str(e)}")
            print("   Check SENDER_EMAIL and SENDER_PASSWORD are correct")
            return False
        except smtplib.SMTPException as e:
            print(f"✗ SMTP error: {str(e)}")
            return False
        except Exception as e:
            print(f"✗ Error sending email: {str(e)}")
            import traceback
            traceback.print_exc()
            return False
 
def main():
    print("=" * 60)
    print("Email Sender")
    print("=" * 60)
    try:
        sender = EmailSender()
        recipients = sender.config.get('recipients', [])
        if not recipients:
            print("\n⚠️  No recipients configured in config/recipients.json")
            print("   Email sending skipped")
            return
        subject = "Load Test Summary Report"
        # Read generated email
        if not os.path.exists("output/email_summary.html"):
            print("\n✗ Error: output/email_summary.html not found")
            print("   Run email generation first")
            return
        with open("output/email_summary.html", 'r') as f:
            body = f.read()
        print(f"\n1. Recipients: {recipients}")
        print(f"2. Subject: {subject}")
        print(f"3. Email body size: {len(body)} bytes")
        print("\n" + "=" * 60)
        sender.send_email(recipients, subject, body)
        print("=" * 60)
    except Exception as e:
        print(f"\n✗ Error: {str(e)}")
        import traceback
        traceback.print_exc()
 
if __name__ == "__main__":
    main()
