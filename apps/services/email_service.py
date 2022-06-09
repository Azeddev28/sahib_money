from django.conf import settings
from django.core.mail import send_mail

from django.template.loader import render_to_string


import threading


class EmailService(threading.Thread):
    def __init__(self, subject, recipients, html_template, template_context):
        threading.Thread.__init__(self)
        self.subject = subject
        self.email_from = settings.EMAIL_HOST_USER
        self.recipients = recipients
        self.html_template = render_to_string(html_template, template_context)

    def send_email(self):
        is_email_sent = send_mail(self.subject,
                                  '',
                                  self.email_from,
                                  self.recipients,
                                  html_message=self.html_template)
        return is_email_sent

    def run(self):
        self.send_email()
