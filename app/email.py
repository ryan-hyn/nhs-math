from flask_mail import Message
from app import mail, app
from flask import render_template
from threading import Thread

# ----------------------------
# DEV MODE TOGGLE
# ----------------------------
DEV_MODE = True  # set to False later for real email


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(subject, sender, recipients, text_body, html_body):
    if DEV_MODE:
        print("\n===== EMAIL DEBUG (DEV MODE) =====")
        print("To:", recipients)
        print("Subject:", subject)
        print("Text body:")
        print(text_body)
        print("=================================\n")
        return

    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    Thread(target=send_async_email, args=(app, msg)).start()


def send_password_reset_email(user):
    token = user.get_reset_password_token()

    send_email(
        '[NHS] Reset Your Password',
        sender=app.config['ADMINS'][0],
        recipients=[user.email],
        text_body=render_template(
            'email/reset_password.txt',
            user=user,
            token=token
        ),
        html_body=render_template(
            'email/reset_password.html',
            user=user,
            token=token
        )
    )
