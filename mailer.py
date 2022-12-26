import smtplib, ssl
from email.message import EmailMessage
import imghdr

# from secret.google_app_password import HOST, PORT, SSL_PORT, USER, PASSWORD
from secret import google_app_password as gap


def send_mail(subject, body, image_path, recipient=gap.USER):
    message = EmailMessage()
    message['Subject'] = subject
    message.set_content(body)

    with open(image_path, 'rb') as file:
        content = file.read()
    message.add_attachment(content, maintype='image', subtype=imghdr.what(None, content))

    gmail = smtplib.SMTP(gap.HOST, gap.PORT)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(gap.USER, gap.PASSWORD)
    gmail.sendmail(gap.USER, recipient, message.as_string())
    gmail.quit()


def old_send_mail(subject, message, receiver=gap.USER):
    context = ssl.create_default_context()

    message = f"Subject: {subject}\n{message}"

    with smtplib.SMTP_SSL(gap.HOST, gap.SSL_PORT, context=context) as server:
        server.login(gap.USER, gap.PASSWORD)
        print(f'sending mail "{subject}" to {receiver}...')
        server.sendmail(gap.USER, receiver, message.encode('utf-8'))
        print('email sent')


if __name__ == '__main__':
    send_mail('test image', 'check this image', 'images/1.png')