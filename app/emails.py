from threading import Thread
from flask_mail import Message
from flask import current_app, render_template


def order_mail_confirmation(app, email, username, book):
    try:
        message = Message('Book order confirmation',
                          sender=current_app.config['MAIL_USERNAME'],
                          recipients=['cristianndan14@gmail.com'])
        message.html = render_template(
            'emails/order_confirmation.html',
            username=username,
            book=book
        )
        thread = Thread(target=send_email_async, args=[app, email, message])
        thread.start()
    except Exception as ex:
        raise Exception(ex)


def send_email_async(app, mail, message):
    with app.app_context():
        mail.send(message)
