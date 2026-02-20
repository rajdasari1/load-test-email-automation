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
        self.config = self.load_config(config_path)
        self.metrics = {}
    def load_config(self, config_path):
        """Load recipient and email configuration"""
        with open(config_path, 'r') as f:
            return json.load(f)
    def parse_csv(self):
        """Parse CSV file and extract key metrics"""
        with open(self.csv_file, 'r') as f:
            reader = csv.DictReader(f)
            data = list(reader)
        # Extract metrics (customize based on your CSV structure)
        self.metrics = {
            'total_requests': len(data),
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'data': data
        }
        return self.metrics
    def generate_email_body(self):
        """Generate professional email body"""
        email_template = f"""
<html>
<body style="font-family: Arial, sans-serif;">
<h2>Load Test Summary Report</h2>
<p>Generated: {self.metrics['timestamp']}</p>
<h3>Key Metrics:</h3>
<ul>
<li>Total Requests: {self.metrics.get('total_requests', 0)}</li>
</ul>
<h3>Detailed Results:</h3>
<table border="1" style="border-collapse: collapse; width: 100%;">
<tr style="background-color: #f2f2f2;">
<th style="padding: 8px;">Metric</th>
<th style="padding: 8px;">Value</th>
</tr>
        """
        # Add data rows
        for row in self.metrics.get('data', [])[:10]:  # Show first 10 rows
            email_template += "<tr>"
            for key, value in row.items():
                email_template += f"<td style='padding: 8px;'>{value}</td>"
            email_template += "</tr>"
        email_template += """
</table>
<p><strong>Next Steps:</strong> Review the detailed metrics and take appropriate action.</p>
<p>Best regards,<br>Performance Testing Team</p>
</body>
</html>
        """
        return email_template
    def save_email(self, output_path="output/email_summary.html"):
        """Save generated email to file"""
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w') as f:
            f.write(self.generate_email_body())
        print(f"Email saved to {output_path}")
        return output_path
    def get_recipients(self):
        """Get email recipient list"""
        return self.config.get('recipients', [])
 
def main():
    # Example usage
    csv_file = "csv_files/load_test_results.csv"
    if not os.path.exists(csv_file):
        print(f"Error: {csv_file} not found. Please add your CSV file to the csv_files/ directory.")
        return
    generator = LoadTestEmailGenerator(csv_file)
    generator.parse_csv()
    generator.save_email()
    recipients = generator.get_recipients()
    print(f"Email ready to send to: {', '.join(recipients)}")
 
if __name__ == "__main__":
    main()
