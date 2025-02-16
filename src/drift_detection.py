import pandas as pd
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset
import sys
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SMTP_SERVER = "smtp.gmail.com"  
SMTP_PORT = 587
EMAIL_SENDER = "ghorbelmahdi0@gmail.com"  
EMAIL_PASSWORD = "asba"  
EMAIL_RECEIVER = "mehdi.ghorbel@insat.ucar.tn"  # ✅ Alert recipient

def send_email_alert():
    subject = " Data Drift Alert: Retraining Required"
    body = "Data drift has been detected in your pipeline. The model will be retrained."

    msg = MIMEMultipart()
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())
        server.quit()
        print("Email alert sent successfully!")
    except Exception as e:
        print(f" Error sending email: {e}")

#  Paths to data
REFERENCE_DATA = "data/reference.csv"
NEW_DATA = "data/new_data.csv"

# Load datasets
reference_data = pd.read_csv(REFERENCE_DATA)
new_data = pd.read_csv(NEW_DATA)

#  Run drift detection
report = Report(metrics=[DataDriftPreset()])
report.run(reference_data=reference_data, current_data=new_data)

drift_result = report.as_dict()

if drift_result["metrics"][0]["result"]["dataset_drift"]:
    print(" Data drift detected! Sending email alert...")
    send_email_alert()  
    sys.exit(1)  # 
else:
    print(" No drift detected. Exiting with code 0.")
    sys.exit(0)  

if __name__ == "__main__":
    detect_drift()
    
 