from imports_variables import *
import imports_variables as vars
import verify_db as our_db

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
    email_user_auth, rfid_uid
    while True:
        msg = subscribe.simple("IoTlab/RFID", hostname="192.168.167.140")
        print("%s %s" % (msg.topic, msg.payload))

        tag_value = msg.payload.decode('utf-8')

        if((our_db.check_user_rfid(vars.rfid_uid) and vars.email_user_auth == False) and vars.user_changed == True):
           send_email()
           vars.email_user_auth = True
           vars.user_changed = False
        else:
        # elif(our_db.check_user_rfid(vars.rfid_uid) == False and vars.email_user_auth == False):
            vars.email_user_auth = False
        time.sleep(1)