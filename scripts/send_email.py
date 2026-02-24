import smtplib
import json
import os
import sys
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
 
def load_config():
    """Load configuration from config.json"""
    try:
        with open('config.json', 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading config.json: {e}")
        return {}
 
def send_email(email_body, recipient_list, subject):
    """
    Send email via SMTP
    """
    # Get credentials from environment variables
    sender_email = os.getenv('SENDER_EMAIL')
    sender_password = os.getenv('SENDER_PASSWORD')
    smtp_host = os.getenv('SMTP_HOST')
    smtp_port = os.getenv('SMTP_PORT', '587')
    # Load config for fallback values
    config = load_config()
    # Use environment variables, fallback to config
    if not smtp_host:
        smtp_host = config.get('smtp_host')
    if not smtp_port:
        smtp_port = config.get('smtp_port', 587)
    # Validate credentials
    print("=" * 60)
    print("Email Sender")
    print("=" * 60)
    print(f"\n1. Recipients: {recipient_list}")
    print(f"2. Subject: {subject}")
    print(f"3. Email body size: {len(email_body)} bytes")
    print(f"4. SMTP Host: {smtp_host}")
    print(f"5. SMTP Port: {smtp_port}")
    print("\n" + "=" * 60)
    # Check if all required variables are set
    if not sender_email:
        print("❌ ERROR: SENDER_EMAIL not set")
        return False
    if not sender_password:
        print("❌ ERROR: SENDER_PASSWORD not set")
        return False
    if not smtp_host:
        print("❌ ERROR: SMTP_HOST not set")
        return False
    try:
        # Convert port to integer
        smtp_port = int(smtp_port)
        # Create message
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = sender_email
        message["To"] = ", ".join(recipient_list)
        # Attach HTML content
        part = MIMEText(email_body, "html")
        message.attach(part)
        print(f"\n📧 Sending email to {len(recipient_list)} recipient(s)...")
        print(f"🔗 Connecting to {smtp_host}:{smtp_port}...")
        # Connect to SMTP server
        server = smtplib.SMTP(smtp_host, smtp_port, timeout=10)
        print(f"🔐 Starting TLS encryption...")
        server.starttls()
        print(f"🔑 Authenticating with sender email...")
        server.login(sender_email, sender_password)
        print(f"✉️  Sending email...")
        server.sendmail(sender_email, recipient_list, message.as_string())
        server.quit()
        print(f"\n✅ Email sent successfully to: {', '.join(recipient_list)}")
        return True
    except smtplib.SMTPAuthenticationError as e:
        print(f"\n❌ SMTP Authentication Error: {e}")
        print("   → Check SENDER_EMAIL and SENDER_PASSWORD")
        return False
    except smtplib.SMTPException as e:
        print(f"\n❌ SMTP error: {e}")
        return False
    except ConnectionError as e:
        print(f"\n❌ Connection error: {e}")
        print(f"   → Check SMTP_HOST ({smtp_host}) and SMTP_PORT ({smtp_port})")
        return False
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        return False
 
if __name__ == "__main__":
    config = load_config()
    # Sample email body for testing
    email_body = "<h1>Test Email</h1><p>This is a test.</p>"
    recipient_list = config.get('recipient_list', [])
    subject = config.get('email_subject', 'Test Email')
    if not recipient_list:
        print("❌ No recipients configured in config.json")
        sys.exit(1)
    success = send_email(email_body, recipient_list, subject)
    sys.exit(0 if success else 1)
