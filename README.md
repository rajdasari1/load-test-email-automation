# Load Test Email Automation
 
Automated system to generate and send load test summary emails using CSV data and GitHub Actions.
 
## 📋 Features
- Parse CSV test result files
- Generate professional HTML email summaries
- Automatically send emails to stakeholders
- Schedule periodic reports
- Manual trigger capability
 
## 🚀 Quick Start
 
### Prerequisites
- Python 3.8+
- GitHub account
- Email account with app-specific password (for SMTP)
 
### Setup Instructions
 
1. **Clone the repository**
   ```bash
   git clone https://github.com/tandmounika/load-test-email-automation.git
   cd load-test-email-automation
   ```
 
2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```
 
3. **Configure email settings**
   - Copy `config/.env.example` to `config/.env`
   - Update with your SMTP credentials
 
4. **Add recipient emails**
   - Edit `config/recipients.json`
   - Add your stakeholder email addresses
 
5. **Add your CSV file**
   - Place your load test CSV in `csv_files/` directory
 
6. **Configure GitHub Secrets**
   - Go to repository Settings → Secrets and variables → Actions
   - Add SMTP credentials
 
7. **Run the workflow**
   - Go to Actions tab → Select "Generate and Send Load Test Email"
   - Click "Run workflow"
 
## 📁 Project Structure
```
├── csv_files/          # Store your CSV test data
├── scripts/            # Python automation scripts
├── config/             # Configuration files
├── templates/          # Email templates
├── .github/workflows/  # GitHub Actions workflows
└── output/             # Generated emails
```
 
## 🔧 Configuration
 
### recipients.json
```json
{
  "recipients": ["email1@company.com", "email2@company.com"],
  "sender": "your-email@company.com",
  "subject_template": "Load Test Summary - {date}"
}
```
 
## 🏃 Running Manually
 
```bash
# Generate email from CSV
python scripts/generate_email.py
 
# Send email
python scripts/send_email.py
```
 
## 📅 Scheduled Execution
 
The workflow runs automatically every Monday at 9 AM UTC. Modify the cron schedule in `.github/workflows/load-test-email.yml` to change timing.
 
## 🔐 Security Notes
- Never commit `.env` file with real credentials
- Use GitHub Secrets for sensitive data
- Consider using organization-managed SMTP service
- Use app-specific passwords, not account passwords
 
## 📧 Email Service Providers
 
### Gmail
- SMTP Server: `smtp.gmail.com`
- Port: `587`
- Generate app-specific password: https://myaccount.google.com/apppasswords
 
### Outlook
- SMTP Server: `smtp.office365.com`
- Port: `587`
 
### SendGrid
- SMTP Server: `smtp.sendgrid.net`
- Port: `587`
- Username: `apikey`
- Password: Your SendGrid API key
 
## 🐛 Troubleshooting
 
**"Connection refused" error**
- Check SMTP server and port are correct
- Verify firewall isn't blocking port 587
 
**"Authentication failed"**
- Ensure email credentials are correct
- Use app-specific password (not account password)
 
**"CSV file not found"**
- Verify CSV is in `csv_files/` directory
- Check file name in script
 
## 📝 Customization
 
Edit `scripts/generate_email.py` to customize:
- CSV parsing logic
- Email template format
- Metric calculations
- Report layout
