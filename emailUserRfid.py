from imports_variables import *
import imports_variables as vars

def send_email():
    current_time = datetime.now()
    formatted_time = current_time.strftime("%H:%M")
    subject = "User Enetered"
    body = "User " + vars.user_id + " has enetered at " + formatted_time

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls() 
            server.login(sender_email, sender_password)  
            server.send_message(msg) 
            date_email_sent = datetime.now()
            print("User entered Email sent successfully!")
            time.sleep(5) 
            capture_email(date_email_sent)
    except Exception as e:
        print(f"Error sending email: {e}")

def loop():