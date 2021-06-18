from django.core.mail import EmailMessage
from django.conf import settings

import datetime


class MailSender:
    subject = 'Система управления "Мой дом 24"'

    def __init__(self, user, file, ticket_number):
        self.user = user
        self.file = file
        self.ticket_number = ticket_number

    def send_email(self):
        from_email = settings.EMAIL_HOST_USER
        to = self.user.email
        email = EmailMessage(
            self.subject,
            'Квитанция на оплату',
            from_email,
            [to],
            headers={'Reply-To': from_email}
        )
        email.attach(f'{datetime.date.today()}_ticket_{self.ticket_number}', self.file.getvalue(), 'application/pdf')
        email.send()
