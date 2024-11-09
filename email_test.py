import smtplib

smtp_host = "smtp.gmail.com"
smtp_port = 587
smtp_user = "firebrigadedatascientest2024@gmail.com"
smtp_password = "_PTT_data%"

try:
    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.starttls()
        server.login(smtp_user, smtp_password)
        print("Login successful")
except smtplib.SMTPAuthenticationError as e:
    print("Authentication error:", e)/home/ubuntu/DST_MLOPS_03_Airflow/DST_MLOPS_03_Airflow