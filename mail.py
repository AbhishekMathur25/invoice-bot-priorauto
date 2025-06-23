import smtplib
from email.message import EmailMessage
import os
from datetime import datetime

# === CONFIG ===
SENDER_EMAIL = 'your_email@gmail.com'
SENDER_PASSWORD = 'your_app_password'  # Use App Password (not your Gmail password)
RECEIVER_EMAIL = 'receiver@example.com'
# Set EXCEL_FILE to today's file
EXCEL_FILE = os.path.join('invoices', f"purchases_{datetime.now().strftime('%d-%b-%y')}.xlsx")

# === EMAIL SETUP ===
msg = EmailMessage()
msg['Subject'] = '📊 Daily Excel Report'
msg['From'] = SENDER_EMAIL
msg['To'] = RECEIVER_EMAIL
msg.set_content('Please find attached the Excel report.')

# === ATTACH FILE ===
with open(EXCEL_FILE, 'rb') as f:
    file_data = f.read()
    file_name = os.path.basename(EXCEL_FILE)

msg.add_attachment(file_data, maintype='application',
                   subtype='vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                   filename=file_name)

# === SEND EMAIL ===
with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login(SENDER_EMAIL, SENDER_PASSWORD)
    smtp.send_message(msg)

print("✅ Email sent successfully!")
