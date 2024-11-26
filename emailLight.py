from imports_variables import *
import imports_variables as vars

def send_email():
    current_time = datetime.now()
    formatted_time = current_time.strftime("%H:%M")

    subject = "Light Alert"
    vars.email_body = f"The light was turned on at {formatted_time}"

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.attach(MIMEText(vars.email_body, 'plain'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls() 
            server.login(sender_email, sender_password)  
            server.send_message(msg) 
            date_email_sessnt = datetime.now()
            print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")

def loop():
    while True:
        # msg = subscribe.simple("IoTlab/EPS32", hostname="192.168.167.140")
        msg = subscribe.simple("IoTlab/EPS32", hostname="192.168.167.140")
        msgrf = subscribe.simple("IoTlab/RFID", hostname="192.168.167.140")
        print("%s %s" % (msg.topic, msg.payload))
        print("%s %s" % (msgrf.topic, msgrf.payload))

        vars.light_value = int(msg.payload.decode('utf-8'))

        if(vars.light_value <= vars.light_threshold and not vars.email_sent):
           send_email()
           vars.email_sent = True
        elif(vars.light_value > 400):
            vars.email_sent = False
        time.sleep(1)