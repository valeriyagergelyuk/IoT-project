import smtplib, ssl, getpass

port = 465 # For SSL
port2 = 1026
#password = getpass.getpass("Type your password and press enter: ")

#sudo python -m smtpd -c DebuggingServer -n localhost:1026 command to run to make server (use data not school wifi)

# ucgu qkwh ltab zapt Go to app password on your google account to generate one
password = "ucgu qkwh ltab zapt"

sender_email = "moars700@gmail.com"  # Enter your address
receiver_email = "giannouleaschris@gmail.com"  # Enter receiver address
message = """\
Subject: Hi there

This message is sent from Python."""

# Create a secure SSL context
context = ssl.create_default_context()

with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
    server.login("moars700@gmail.com", password)
    server.sendmail(sender_email, receiver_email, message)
    
with smtplib.SMTP("localhost", port2) as server:
    server.sendmail(sender_email, receiver_email, message)
    
    
