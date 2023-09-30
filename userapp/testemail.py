import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio

# Local SMTP server configuration
smtp_server = 'localhost'
smtp_port = 4501  # You can choose a port number

# Sender and recipient email addresses
from_email = 'sender@192.168.0.53.com'
#to_email = 'parentcontrols@proton.me'
to_email = 'contact@parentcontrols.win'
#to_email = 'thomasdh1996@gmail.com'

# Email content
subject = 'Hello from Python'
message = 'This is a test email sent from Python using a local SMTP server.'

# Create the email message
msg = MIMEMultipart()
msg['From'] = from_email
msg['To'] = to_email
msg['Subject'] = subject
msg.attach(MIMEText(message, 'plain'))

# Optionally, you can attach files (e.g., images or audio)
# For example, to attach an image:
# with open('image.jpg', 'rb') as image_file:
#     image = MIMEImage(image_file.read(), name='image.jpg')
#     msg.attach(image)
try:
    # Connect to the local SMTP server
    server = smtplib.SMTP(smtp_server, smtp_port)
    #server = smtplib.SMTP("localhost")

    # Send the email
    server.sendmail(from_email, to_email, msg.as_string())
    print("Email sent successfully!")

except Exception as e:
    print(f"An error occurred: {str(e)}")

finally:
    server.quit()

