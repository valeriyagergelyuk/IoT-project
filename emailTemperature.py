from imports_variables import *
import imports_variables as vars

def send_email():
    subject = "Temperature Alert"
    body = "The temperature has exceeded 24 degrees Celsius. Would You like to turn on the fan? Reply with Yes to turn on the fan."

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
            print("Email sent successfully!")
            time.sleep(5) 
            capture_email(date_email_sent)
    except Exception as e:
        print(f"Error sending email: {e}")

def capture_email(date_email_sent):
    # global dht_is_running
    yes_mail_received = False

    # Allows the probing to work while waiting for email
    if not vars.dht_is_running:
        vars.dht_is_running = True
        dht_thread = threading.Thread(target=dht_loop, daemon=True)
        dht_thread.start()

    mail = imaplib.IMAP4_SSL('smtp.gmail.com')
    mail.login(sender_email, sender_password)

    #looping while the email has not been received
    while yes_mail_received == False:
        
        mail.select('inbox')
        status, data = mail.search(None, 'SUBJECT "Temperature Alert"')
        
        #list of emails
        mails = data[0].split()

        #looping through the emails if there are any
        if mails:
            for email_id in reversed(mails):
                
                status, info = mail.fetch(email_id, '(RFC822)')
                
                for response_part in info:
                    if isinstance(response_part, tuple):
                        # Parse the email content
                        message = BytesParser(policy=policy.default).parsebytes(response_part[1])
                        
                        mail_from = message['from']
                        date_str = message["Date"]
                        mail_body = None
                        first_line = None

                        # Extracting the body
                        if message.is_multipart():
                            for part in message.iter_parts():
                                if part.get_content_type() == 'text/plain':
                                    mail_body = part.get_payload(decode=True).decode().strip()
                                    # Makng sure to only get one line
                                    first_line = mail_body.splitlines()[0]
                                    break
                                    
                        print(mail_from)
                        print(first_line)
                        print(date_str)

                    if first_line == 'Yes':
                        yes_mail_received = True
                        print("Fan Turning On")
                        vars.fan_on = True
                        # Activates the motor
                        toggle_motor(first_line)
                        # this will get rid of the emai after it has seen it
                        mail.store(email_id, '+FLAGS', '\\Deleted')
                        mail.expunge()

                    elif first_line != None:
                        yes_mail_received = False
                        print("Fan Not Turning On")
                        mail.store(email_id, '+FLAGS', '\\Deleted')
                        mail.expunge()

                if(yes_mail_received == True):
                    break
    # Stops the thread
    vars.dht_is_running = False
        
        ## Now the email will wait for a yes always, but if user says no, it won't resend if it dropps down to below 24,
        ## then comes back up uptill the user says yes, should that be changed?

        ## not sure if we should have a limiter of some kind incase the user never replies or the email just fails to send
        ## Rn if something happens to the email where it just never gets sent, it will wait infinty for the response (Atleast i think it would)
        ## Maybe there shuold be something to just resend it after it checks for a response 5 times

def dht_loop():
    global sumCnt, okCnt

    while vars.dht_is_running:
        sumCnt += 1
        chk = dht.readDHT11()   
        if chk == 0:
            okCnt += 1      
        
        okRate = 100.0 * okCnt / sumCnt
        # Update humidity and temperature for the web server
        vars.hum = random.randint(50,60) #dht.getHumidity()
        vars.temp = random.randint(19,24)#dht.getTemperature()
        
        print("sumCnt : %d, \t okRate : %.2f%% "%(sumCnt, okRate))
        print("chk : %d, \t Humidity : %.2f, \t Temperature : %.2f "%(chk, vars.hum, vars.temp))

        time.sleep(3)

def toggle_motor(emailResult):
    if emailResult == 'Yes':
        GPIO.output(Motor1, GPIO.HIGH)  # Sets it on
        # Handles direction
        GPIO.output(Motor2, GPIO.LOW)
        GPIO.output(Motor3, GPIO.HIGH) 
    else:
        vars.fan_on = False
        GPIO.output(Motor1, GPIO.LOW)  # Sets it off

def loop():
    global sumCnt, okCnt
    email_sent = False  # Flag to track if the email has been sent

    while threads_active:
        sumCnt += 1
        chk = dht.readDHT11()   
        if chk == 0:
            okCnt += 1      
        
        okRate = 100.0 * okCnt / sumCnt
        # Update humidity and temperature for the web server
        vars.hum = random.randint(50,60) #dht.getHumidity()
        vars.temp = random.randint(19,24)#dht.getTemperature()

        print("sumCnt : %d, \t okRate : %.2f%% "%(sumCnt, okRate))
        print("chk : %d, \t Humidity : %.2f, \t Temperature : %.2f "%(chk,vars.hum , vars.temp))

        # Check temperature and send email if necessary
        if vars.temp > vars.temp_threshold and not email_sent:
            send_email() 
            email_sent = True  # Set flag to indicate email has been sent
        elif vars.temp <= 22:
            email_sent = False  # Reset the flag if temperature goes below 24
            toggle_motor('off')
        time.sleep(3)