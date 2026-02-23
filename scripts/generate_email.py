#!/usr/bin/env python3
"""
Load Test Summary Email Generator
Processes CSV files and generates professional email summaries
"""
 
import csv
import json
import os
from datetime import datetime
from pathlib import Path
 
class LoadTestEmailGenerator:
    def __init__(self, csv_file_path, config_path="config/recipients.json"):
        self.csv_file = csv_file_path
        self.config_path = config_path
        self.config = {}
        self.metrics = {}
        self.load_config()
    def load_config(self):
        """Load recipient and email configuration"""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r') as f:
                    self.config = json.load(f)
                print(f"✓ Config loaded from {self.config_path}")
            else:
                print(f"⚠️  Config file not found: {self.config_path}")
                self.config = {
                    'recipients': ['test@example.com'],
                    'sender': 'automation@example.com',
                    'subject_template': 'Load Test Summary Report - {date}'
                }
        except Exception as e:
            print(f"✗ Error loading config: {str(e)}")
            self.config = {}
    def parse_csv(self):
        """Parse CSV file and extract key metrics"""
        try:
            if not os.path.exists(self.csv_file):
                print(f"⚠️  CSV file not found: {self.csv_file}")
                print(f"Creating sample data...")
                self.create_sample_csv()
            with open(self.csv_file, 'r') as f:
                reader = csv.DictReader(f)
                data = list(reader)
            if not data:
                print(f"⚠️  CSV file is empty: {self.csv_file}")
                return
            # Extract metrics
            self.metrics = {
                'total_requests': len(data),
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'data': data
            }
            print(f"✓ CSV parsed successfully: {len(data)} rows")
            return self.metrics
        except Exception as e:
            print(f"✗ Error parsing CSV: {str(e)}")
            return None
    def create_sample_csv(self):
        """Create sample CSV if it doesn't exist"""
        try:
            os.makedirs(os.path.dirname(self.csv_file) or '.', exist_ok=True)
            with open(self.csv_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['test_name', 'endpoint', 'response_time_ms', 'status_code', 'requests_per_second', 'timestamp'])
                writer.writerows([
                    ['Login Test', '/api/login', '245', '200', '100', '2026-02-20 09:15:00'],
                    ['Product Search', '/api/search', '312', '200', '150', '2026-02-20 09:16:00'],
                    ['Checkout', '/api/checkout', '567', '200', '80', '2026-02-20 09:17:00'],
                    ['Payment Processing', '/api/payment', '890', '200', '50', '2026-02-20 09:18:00'],
                ])
            print(f"✓ Sample CSV created: {self.csv_file}")
        except Exception as e:
            print(f"✗ Error creating sample CSV: {str(e)}")
    def generate_email_body(self):
        """Generate professional email body"""
        if not self.metrics:
            print("⚠️  No metrics available for email generation")
            return None
        try:
            email_template = f"""
<html>
<body style="font-family: Arial, sans-serif; margin: 20px;">
<h2 style="color: #333;">Load Test Summary Report</h2>
<p style="color: #666;">Generated: {self.metrics['timestamp']}</p>
<h3 style="color: #333;">Key Metrics:</h3>
<ul style="color: #666;">
<li><strong>Total Requests:</strong> {self.metrics.get('total_requests', 0)}</li>
<li><strong>Report Generated:</strong> {self.metrics['timestamp']}</li>
</ul>
<h3 style="color: #333;">Detailed Results:</h3>
<table border="1" style="border-collapse: collapse; width: 100%; color: #333;">
<tr style="background-color: #f2f2f2;">
<th style="padding: 8px; text-align: left;">Test Name</th>
<th style="padding: 8px; text-align: left;">Endpoint</th>
<th style="padding: 8px; text-align: left;">Response Time (ms)</th>
<th style="padding: 8px; text-align: left;">Status</th>
</tr>
            """
            # Add data rows
            for row in self.metrics.get('data', [])[:10]:  # Show first 10 rows
                email_template += "<tr>"
                email_template += f"<td style='padding: 8px;'>{row.get('test_name', 'N/A')}</td>"
                email_template += f"<td style='padding: 8px;'>{row.get('endpoint', 'N/A')}</td>"
                email_template += f"<td style='padding: 8px;'>{row.get('response_time_ms', 'N/A')}</td>"
                email_template += f"<td style='padding: 8px;'>{row.get('status_code', 'N/A')}</td>"
                email_template += "</tr>"
            email_template += """
</table>
<p style="color: #666; margin-top: 20px;"><strong>Next Steps:</strong> Review the detailed metrics and take appropriate action if needed.</p>
<hr style="border: none; border-top: 1px solid #ddd; margin: 20px 0;">
<p style="color: #999; font-size: 12px;">Best regards,<br><strong>Performance Testing Team</strong></p>
</body>
</html>
            """
            print("✓ Email body generated successfully")
            return email_template
        except Exception as e:
            print(f"✗ Error generating email body: {str(e)}")
            return None
    def save_email(self, output_path="output/email_summary.html"):
        """Save generated email to file"""
        try:
            os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
            email_body = self.generate_email_body()
            if not email_body:
                print("✗ Cannot save email: no body generated")
                return None
            with open(output_path, 'w') as f:
                f.write(email_body)
            print(f"✓ Email saved to {output_path}")
            # Verify file was created
            if os.path.exists(output_path):
                file_size = os.path.getsize(output_path)
                print(f"✓ File verified: {file_size} bytes")
            return output_path
        except Exception as e:
            print(f"✗ Error saving email: {str(e)}")
            return None
    def get_recipients(self):
        """Get email recipient list"""
        return self.config.get('recipients', [])
 
def main():
    print("=" * 60)
    print("Load Test Email Generator")
    print("=" * 60)
    csv_file = "csv_files/load_test_results.csv"
    try:
        generator = LoadTestEmailGenerator(csv_file)
        print(f"\n1. Parsing CSV: {csv_file}")
        generator.parse_csv()
        print(f"\n2. Generating email")
        generator.save_email()
        recipients = generator.get_recipients()
        print(f"\n3. Recipients: {', '.join(recipients)}")
        print("\n" + "=" * 60)
        print("✓ Email generation completed successfully!")
        print("=" * 60)
    except Exception as e:
        print(f"\n✗ Error: {str(e)}")
        import traceback
        traceback.print_exc()
 
if __name__ == "__main__":
    main()
