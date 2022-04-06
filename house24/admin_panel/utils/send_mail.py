from django.core.mail import EmailMessage
from django.conf import settings
from django.utils.translation import gettext_lazy as _

import datetime


class MailSender:
    subject = _('Management system "My House 24"')

    def __init__(self, user, file, ticket_number):
        self.user = user
        self.file = file
        self.ticket_number = ticket_number

    def send_email(self):
        from_email = settings.EMAIL_HOST_USER
        to = self.user.email
        email = EmailMessage(
            self.subject,
            _('Receipt for payment'),
            from_email,
            [to],
            headers={'Reply-To': from_email}
        )
        email.attach(f'{datetime.date.today()}_ticket_{self.ticket_number}', self.file.getvalue(), 'application/pdf')
        email.send()
